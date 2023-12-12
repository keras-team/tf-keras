"""Tests for calling optimizer on ParameterServerStrategy."""

import os

import tensorflow.compat.v2 as tf
from absl.testing import parameterized

import tf_keras as keras
from tf_keras.optimizers import adadelta
from tf_keras.optimizers import adagrad
from tf_keras.optimizers import adam
from tf_keras.optimizers import adamax
from tf_keras.optimizers import adamw
from tf_keras.optimizers import ftrl
from tf_keras.optimizers import lion
from tf_keras.optimizers import nadam
from tf_keras.optimizers import rmsprop
from tf_keras.optimizers import sgd
from tf_keras.utils import dataset_creator
from tf_keras.utils import losses_utils

ds_combinations = tf.__internal__.distribute.combinations

STRATEGIES = [
    ds_combinations.parameter_server_strategy_3worker_2ps_cpu,
    ds_combinations.parameter_server_strategy_3worker_2ps_1gpu,
]

adadelta_fn = tf.__internal__.test.combinations.NamedObject(
    "adadelta",
    lambda: adadelta.Adadelta(
        0.002, use_ema=True, ema_overwrite_frequency=None
    ),
)
adagrad_fn = tf.__internal__.test.combinations.NamedObject(
    "adagrad", lambda: adagrad.Adagrad(0.002)
)
adam_fn = tf.__internal__.test.combinations.NamedObject(
    "adam", lambda: adam.Adam(0.002)
)
adamax_fn = tf.__internal__.test.combinations.NamedObject(
    "adamax", lambda: adamax.Adamax(0.002)
)
adamw_fn = tf.__internal__.test.combinations.NamedObject(
    "adamw", lambda: adamw.AdamW(0.002, weight_decay=0.004)
)
ftrl_fn = tf.__internal__.test.combinations.NamedObject(
    "ftrl", lambda: ftrl.Ftrl(0.002)
)
lion_fn = tf.__internal__.test.combinations.NamedObject(
    "lion", lambda: lion.Lion(0.002)
)
nadam_fn = tf.__internal__.test.combinations.NamedObject(
    "experimentnadam", lambda: nadam.Nadam(0.002)
)
rmsprop_fn = tf.__internal__.test.combinations.NamedObject(
    "rmsprop", lambda: rmsprop.RMSprop(0.002)
)
sgd_fn = tf.__internal__.test.combinations.NamedObject(
    "sgdaverage",
    lambda: sgd.SGD(0.002, use_ema=True, ema_overwrite_frequency=1),
)

OPTIMIZER_FN = [
    adadelta_fn,
    adagrad_fn,
    adam_fn,
    adamax_fn,
    adamw_fn,
    ftrl_fn,
    lion_fn,
    nadam_fn,
    rmsprop_fn,
    sgd_fn,
]


# TODO(b/228209527): Combine this test with optimizer_test after
# fixing the NCCL issue.
class OptimizerPssTest(tf.test.TestCase, parameterized.TestCase):
    def _get_model(self):
        return keras.Sequential(
            [keras.layers.Input(shape=(1,)), keras.layers.Dense(1)]
        )

    def _get_dataset_fn(self):
        def dataset_fn(_):
            x, y = [1, 1, 1, 0, 0, 0], [1, 1, 1, 0, 0, 0]
            ds = tf.data.Dataset.from_tensor_slices((x, y))
            ds = ds.repeat().batch(6)
            return ds

        return dataset_fn

    def _verify_accumulators_updated(self, optimizer):
        variables = optimizer.variables
        for var in variables:
            if "iteration" not in var.name and "learning_rate" not in var.name:
                # Find a variable not iteration or learning_rate, and verify its
                # value is updated (not 0).
                if isinstance(var, tf.__internal__.distribute.ShardedVariable):
                    for shard in var.variables:
                        self.assertNotAllEqual(shard, 0)
                else:
                    self.assertNotAllEqual(var, 0)

    @ds_combinations.generate(
        tf.__internal__.test.combinations.combine(
            strategy=STRATEGIES, optimizer_fn=OPTIMIZER_FN
        )
    )
    def testGetGradientsInModelPss(self, strategy, optimizer_fn):
        with strategy.scope():
            model = self._get_model()
            optimizer = optimizer_fn()
        ds_fn = self._get_dataset_fn()
        if isinstance(strategy, tf.distribute.ParameterServerStrategy):
            ds = dataset_creator.DatasetCreator(ds_fn)
        else:
            ds = ds_fn(None)
        model.compile(loss="mse", optimizer=optimizer)
        model.fit(ds, epochs=1, steps_per_epoch=5)

        self._verify_accumulators_updated(optimizer)

    @ds_combinations.generate(
        tf.__internal__.test.combinations.combine(
            strategy=STRATEGIES, optimizer_fn=OPTIMIZER_FN
        )
    )
    def testGetGradientsInCustomTrainingLoopPss(self, strategy, optimizer_fn):
        coordinator = tf.distribute.experimental.coordinator.ClusterCoordinator(
            strategy
        )

        with strategy.scope():
            model = self._get_model()
            optimizer = optimizer_fn()

            def per_worker_dataset_fn():
                return strategy.distribute_datasets_from_function(
                    self._get_dataset_fn()
                )

            ds = coordinator.create_per_worker_dataset(per_worker_dataset_fn)

            @tf.function
            def train_step(iterator):
                def replica_fn(data):
                    features, labels = data
                    with tf.GradientTape() as tape:
                        output = model(tf.expand_dims(features, axis=1))
                        loss = keras.losses.MeanSquaredError(
                            reduction=losses_utils.ReductionV2.NONE
                        )(labels, output)
                    grads = tape.gradient(loss, model.trainable_variables)
                    optimizer.apply_gradients(
                        zip(grads, model.trainable_variables)
                    )

                strategy.run(replica_fn, args=(next(iterator),))

            for _ in range(3):
                coordinator.schedule(train_step, args=(iter(ds),))
                coordinator.join()
            self.assertEqual(self.evaluate(optimizer.iterations), 3)
            self._verify_accumulators_updated(optimizer)

    @ds_combinations.generate(
        tf.__internal__.test.combinations.combine(
            strategy=STRATEGIES,
            shard_config=[
                [2, 2],
                [2, 3],
                [3, 2],
                [2, 1],
                [1, 1],
                [1, 2],
                [1, 3],
            ],
        )
    )
    def testCheckpointShardedVariable(self, strategy, shard_config):
        # Data are embedding indices near shard boundaries for 2 or 3 shards
        test_indices = [33, 34, 49, 50, 66, 67]

        def dataset_fn(_):
            x, y = [[index] for index in test_indices], [1, 1, 1, 0, 0, 0]
            ds = tf.data.Dataset.from_tensor_slices((x, y))
            ds = ds.repeat().batch(6)
            return ds

        vocab_size = 100
        embed_dim = 32

        def get_model():
            return keras.Sequential(
                [
                    keras.layers.Embedding(vocab_size, embed_dim),
                    keras.layers.Dense(1, activation="sigmoid"),
                ]
            )

        # Override partitioning
        if shard_config[0] == 1:
            strategy._extended._variable_partitioner = None
        else:
            strategy._extended._variable_partitioner = (
                tf.distribute.experimental.partitioners.FixedShardsPartitioner(
                    shard_config[0]
                )
            )

        # Create model and optimizer
        with strategy.scope():
            model = get_model()
            optimizer = adam.Adam(0.002)

            model.compile(loss="mse", optimizer=optimizer)

            model.build(input_shape=(None, 1))
            model.optimizer.build(model.trainable_variables)

        ds = dataset_creator.DatasetCreator(dataset_fn)
        # Train a bit to update optimizer variables
        model.fit(ds, epochs=1, steps_per_epoch=5)

        self._verify_accumulators_updated(optimizer)

        # Extract optimizer variables to later check they restore properly
        pre_ckpt_optimizer_values = []
        for var in model.optimizer.variables:
            # Just check the embedding variables
            if var.shape == [vocab_size, embed_dim]:
                for index in test_indices:
                    pre_ckpt_optimizer_values.append(var[index])
        # Adam has 2 slot variables, momentum and velocity
        self.assertLen(pre_ckpt_optimizer_values, 2 * len(test_indices))

        checkpoint_path = os.path.join(self.get_temp_dir(), "model_weights")
        model.save_weights(checkpoint_path)

        # Create new model under different sharding and load checkpoint
        if shard_config[1] == 1:
            strategy._extended._variable_partitioner = None
        else:
            strategy._extended._variable_partitioner = (
                tf.distribute.experimental.partitioners.FixedShardsPartitioner(
                    shard_config[1]
                )
            )
        with strategy.scope():
            model_2 = get_model()
            optimizer_2 = adam.Adam(0.002)
            model_2.compile(loss="mse", optimizer=optimizer_2)
            model_2.build(input_shape=(None, 1))
            model_2.optimizer.build(model_2.trainable_variables)
            model_2.load_weights(checkpoint_path)

        post_ckpt_optimizer_values = []
        for var in model_2.optimizer.variables:
            if var.shape == [vocab_size, embed_dim]:
                for index in test_indices:
                    post_ckpt_optimizer_values.append(var[index])
        self.assertLen(post_ckpt_optimizer_values, 2 * len(test_indices))
        for pre_val, post_val in zip(
            pre_ckpt_optimizer_values, post_ckpt_optimizer_values
        ):
            self.assertAllEqual(pre_val, post_val)

        # Confirm training still functional
        ds = dataset_creator.DatasetCreator(dataset_fn)
        model_2.fit(ds, epochs=1, steps_per_epoch=5)


if __name__ == "__main__":
    tf.__internal__.distribute.multi_process_runner.test_main()
