# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for Bidirectional wrapper."""


import copy

import numpy as np
import tensorflow.compat.v2 as tf
from absl.testing import parameterized

import tf_keras as keras
from tf_keras.engine import base_layer_utils
from tf_keras.layers import core
from tf_keras.layers.rnn.cell_wrappers import ResidualWrapper
from tf_keras.testing_infra import test_combinations
from tf_keras.testing_infra import test_utils

# isort: off
from tensorflow.python.checkpoint import (
    checkpoint as trackable_util,
)
from tensorflow.python.framework import (
    test_util as tf_test_util,
)


class _RNNCellWithConstants(keras.layers.Layer):
    def __init__(self, units, constant_size, **kwargs):
        self.units = units
        self.state_size = units
        self.constant_size = constant_size
        super().__init__(**kwargs)

    def build(self, input_shape):
        self.input_kernel = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer="uniform",
            name="kernel",
        )
        self.recurrent_kernel = self.add_weight(
            shape=(self.units, self.units),
            initializer="uniform",
            name="recurrent_kernel",
        )
        self.constant_kernel = self.add_weight(
            shape=(self.constant_size, self.units),
            initializer="uniform",
            name="constant_kernel",
        )
        super().build(input_shape)

    def call(self, inputs, states, constants):
        [prev_output] = states
        [constant] = constants
        h_input = keras.backend.dot(inputs, self.input_kernel)
        h_state = keras.backend.dot(prev_output, self.recurrent_kernel)
        h_const = keras.backend.dot(constant, self.constant_kernel)
        output = h_input + h_state + h_const
        return output, [output]

    def get_config(self):
        config = {"units": self.units, "constant_size": self.constant_size}
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


class _ResidualLSTMCell(keras.layers.LSTMCell):
    def call(self, inputs, states, training=None):
        output, states = super().call(inputs, states)
        return output + inputs, states


class _AddOneCell(keras.layers.AbstractRNNCell):
    """Increments inputs and state by one on each call."""

    @property
    def state_size(self):
        return 1

    @property
    def output_size(self):
        return 1

    def call(self, inputs, state):
        inputs = tf.reduce_mean(inputs, axis=1, keepdims=True)
        outputs = inputs + 1.0
        state = tf.nest.map_structure(lambda t: t + 1.0, state)
        return outputs, state


@test_combinations.generate(test_combinations.combine(mode=["graph", "eager"]))
class BidirectionalTest(tf.test.TestCase, parameterized.TestCase):
    @parameterized.parameters(["sum", "concat", "ave", "mul"])
    def test_bidirectional(self, mode):
        rnn = keras.layers.SimpleRNN
        samples = 2
        dim = 2
        timesteps = 2
        output_dim = 2
        with self.cached_session():
            x = np.random.random((samples, timesteps, dim))
            target_dim = 2 * output_dim if mode == "concat" else output_dim
            y = np.random.random((samples, target_dim))

            # test with Sequential model
            model = keras.models.Sequential()
            model.add(
                keras.layers.Bidirectional(
                    rnn(output_dim),
                    merge_mode=mode,
                    input_shape=(timesteps, dim),
                )
            )
            model.compile(optimizer="rmsprop", loss="mse")
            model.fit(x, y, epochs=1, batch_size=1)

            # check whether the model variables are present in the
            # trackable list of objects
            checkpointed_object_ids = {
                id(o) for o in trackable_util.list_objects(model)
            }
            for v in model.variables:
                self.assertIn(id(v), checkpointed_object_ids)

            # test compute output shape
            ref_shape = model.layers[-1].output.shape
            shape = model.layers[-1].compute_output_shape(
                (None, timesteps, dim)
            )
            self.assertListEqual(shape.as_list(), ref_shape.as_list())

            # test config
            model.get_config()
            model = keras.models.model_from_json(model.to_json())
            model.summary()

    def test_bidirectional_invalid_init(self):
        x = tf.constant(np.zeros((1, 1)).astype("float32"))
        with self.assertRaisesRegex(
            ValueError,
            "Please initialize `Bidirectional` layer with a "
            "`tf.keras.layers.Layer` instance.",
        ):
            keras.layers.Bidirectional(x)

    def test_bidirectional_weight_loading(self):
        rnn = keras.layers.SimpleRNN
        samples = 2
        dim = 2
        timesteps = 2
        output_dim = 2
        with self.cached_session():
            x = np.random.random((samples, timesteps, dim))
            model = keras.models.Sequential()
            model.add(
                keras.layers.Bidirectional(
                    rnn(output_dim), input_shape=(timesteps, dim)
                )
            )
            y_ref = model.predict(x)
            weights = model.layers[-1].get_weights()
            model.layers[-1].set_weights(weights)
            y = model.predict(x)
            self.assertAllClose(y, y_ref)

    def test_bidirectional_stacked(self):
        # test stacked bidirectional layers
        rnn = keras.layers.SimpleRNN
        samples = 2
        dim = 2
        timesteps = 2
        output_dim = 2
        mode = "sum"

        with self.cached_session():
            x = np.random.random((samples, timesteps, dim))
            target_dim = 2 * output_dim if mode == "concat" else output_dim
            y = np.random.random((samples, target_dim))

            model = keras.models.Sequential()
            model.add(
                keras.layers.Bidirectional(
                    rnn(output_dim, return_sequences=True),
                    merge_mode=mode,
                    input_shape=(timesteps, dim),
                )
            )
            model.add(
                keras.layers.Bidirectional(rnn(output_dim), merge_mode=mode)
            )
            model.compile(loss="mse", optimizer="sgd")
            model.fit(x, y, epochs=1, batch_size=1)

            # test with functional API
            inputs = keras.layers.Input((timesteps, dim))
            output = keras.layers.Bidirectional(
                rnn(output_dim), merge_mode=mode
            )(inputs)
            model = keras.models.Model(inputs, output)
            model.compile(loss="mse", optimizer="sgd")
            model.fit(x, y, epochs=1, batch_size=1)

    def test_bidirectional_statefulness(self):
        # Bidirectional and stateful
        def run_test():
            rnn = keras.layers.SimpleRNN
            samples = 2
            dim = 2
            timesteps = 2
            output_dim = 2
            mode = "sum"

            with self.cached_session():
                x = np.random.random((samples, timesteps, dim))
                target_dim = 2 * output_dim if mode == "concat" else output_dim
                y = np.random.random((samples, target_dim))

                inputs = keras.layers.Input(batch_shape=(1, timesteps, dim))
                bidi_rnn = keras.layers.Bidirectional(
                    rnn(output_dim, stateful=True), merge_mode=mode
                )
                self.assertTrue(bidi_rnn.stateful)
                output = bidi_rnn(inputs)
                model = keras.models.Model(inputs, output)

                y_1 = model.predict(x, batch_size=1)
                model.reset_states()
                y_2 = model.predict(x, batch_size=1)

                self.assertAllClose(y_1, y_2)

                model.compile(loss="mse", optimizer="sgd")
                model.fit(x, y, epochs=1, batch_size=1)

        if tf.executing_eagerly():
            run_test()
        else:
            tf_test_util.enable_output_all_intermediates(run_test)()

    @parameterized.parameters(["sum", "mul", "ave", "concat", None])
    def test_Bidirectional_merged_value(self, merge_mode):
        rnn = keras.layers.LSTM
        samples = 2
        dim = 5
        timesteps = 3
        units = 3
        x = [np.random.rand(samples, timesteps, dim)]

        with self.cached_session():
            if merge_mode == "sum":
                merge_func = lambda y, y_rev: y + y_rev
            elif merge_mode == "mul":
                merge_func = lambda y, y_rev: y * y_rev
            elif merge_mode == "ave":
                merge_func = lambda y, y_rev: (y + y_rev) / 2
            elif merge_mode == "concat":
                merge_func = lambda y, y_rev: np.concatenate(
                    (y, y_rev), axis=-1
                )
            else:
                merge_func = lambda y, y_rev: [y, y_rev]

            # basic case
            inputs = keras.Input((timesteps, dim))
            layer = keras.layers.Bidirectional(
                rnn(units, return_sequences=True), merge_mode=merge_mode
            )
            f_merged = keras.backend.function([inputs], _to_list(layer(inputs)))
            f_forward = keras.backend.function(
                [inputs], [layer.forward_layer(inputs)]
            )
            f_backward = keras.backend.function(
                [inputs],
                [keras.backend.reverse(layer.backward_layer(inputs), 1)],
            )

            y_merged = f_merged(x)
            y_expected = _to_list(merge_func(f_forward(x)[0], f_backward(x)[0]))
            assert len(y_merged) == len(y_expected)
            for x1, x2 in zip(y_merged, y_expected):
                self.assertAllClose(x1, x2, atol=1e-5)

            # test return_state
            inputs = keras.Input((timesteps, dim))
            layer = keras.layers.Bidirectional(
                rnn(units, return_state=True), merge_mode=merge_mode
            )
            f_merged = keras.backend.function([inputs], layer(inputs))
            f_forward = keras.backend.function(
                [inputs], layer.forward_layer(inputs)
            )
            f_backward = keras.backend.function(
                [inputs], layer.backward_layer(inputs)
            )
            n_states = len(layer.layer.states)

            y_merged = f_merged(x)
            y_forward = f_forward(x)
            y_backward = f_backward(x)
            y_expected = _to_list(merge_func(y_forward[0], y_backward[0]))
            assert len(y_merged) == len(y_expected) + n_states * 2
            for x1, x2 in zip(y_merged, y_expected):
                self.assertAllClose(x1, x2, atol=1e-5)

            y_merged = y_merged[-n_states * 2 :]
            y_forward = y_forward[-n_states:]
            y_backward = y_backward[-n_states:]
            for state_birnn, state_inner in zip(
                y_merged, y_forward + y_backward
            ):
                self.assertAllClose(state_birnn, state_inner, atol=1e-5)

    @parameterized.parameters([True, False])
    def test_Bidirectional_with_time_major_input(self, time_major):
        batch_size, time, input_dim = 2, 3, 1
        inputs = tf.zeros((batch_size, time, input_dim))
        # length is [1 2]. Within the batch, the first element has 1 step, and
        # the second element as 2 steps.
        lengths = tf.range(1, 1 + batch_size)
        mask = tf.sequence_mask(lengths, maxlen=time, dtype=tf.float32)

        forward_cell = _AddOneCell(name="forward")
        backward_cell = _AddOneCell(name="backward")

        layer = keras.layers.Bidirectional(
            layer=keras.layers.RNN(
                forward_cell, time_major=time_major, return_sequences=True
            ),
            backward_layer=keras.layers.RNN(
                backward_cell,
                time_major=time_major,
                return_sequences=True,
                go_backwards=True,
            ),
        )

        # Switch to time-major.
        if time_major:
            inputs = tf.transpose(inputs, [1, 0, 2])
            mask = tf.transpose(mask, [1, 0])

        keras_outputs = layer(inputs, mask=mask)
        if time_major:
            keras_outputs = tf.transpose(keras_outputs, [1, 0, 2])

        # expect the first element in batch has 1 step and second element in
        # batch has 2 steps.
        expected_result = np.array(
            [
                [[1.0, 1.0], [0.0, 0.0], [0.0, 0.0]],
                [[1.0, 1.0], [1.0, 1.0], [0.0, 0.0]],
            ]
        )
        self.assertAllClose(expected_result, keras_outputs)

    def test_Bidirectional_dropout(self):
        rnn = keras.layers.LSTM
        samples = 2
        dim = 5
        timesteps = 3
        units = 3
        merge_mode = "sum"
        x = [np.random.rand(samples, timesteps, dim)]

        with self.cached_session():
            inputs = keras.Input((timesteps, dim))
            wrapped = keras.layers.Bidirectional(
                rnn(units, dropout=0.2, recurrent_dropout=0.2),
                merge_mode=merge_mode,
            )
            outputs = _to_list(wrapped(inputs, training=True))

            inputs = keras.Input((timesteps, dim))
            wrapped = keras.layers.Bidirectional(
                rnn(units, dropout=0.2, return_state=True),
                merge_mode=merge_mode,
            )
            outputs = _to_list(wrapped(inputs))

            model = keras.Model(inputs, outputs)
            y1 = _to_list(model.predict(x))
            y2 = _to_list(model.predict(x))
            for x1, x2 in zip(y1, y2):
                self.assertAllClose(x1, x2, atol=1e-5)

    def test_Bidirectional_state_reuse(self):
        rnn = keras.layers.LSTM
        samples = 2
        dim = 5
        timesteps = 3
        units = 3

        with self.cached_session():
            input1 = keras.layers.Input((timesteps, dim))
            layer = keras.layers.Bidirectional(
                rnn(units, return_state=True, return_sequences=True)
            )
            state = layer(input1)[1:]

            # test passing invalid initial_state: passing a tensor
            input2 = keras.layers.Input((timesteps, dim))
            with self.assertRaises(ValueError):
                keras.layers.Bidirectional(rnn(units))(
                    input2, initial_state=state[0]
                )

            # test valid usage: passing a list
            output = keras.layers.Bidirectional(rnn(units))(
                input2, initial_state=state
            )
            model = keras.models.Model([input1, input2], output)
            assert len(model.layers) == 4
            assert isinstance(model.layers[-1].input, list)
            inputs = [
                np.random.rand(samples, timesteps, dim),
                np.random.rand(samples, timesteps, dim),
            ]
            model.predict(inputs)

    def test_Bidirectional_state_reuse_with_np_input(self):
        # See https://github.com/tensorflow/tensorflow/issues/28761 for more
        # detail.
        rnn = keras.layers.LSTM
        samples = 2
        dim = 5
        timesteps = 3
        units = 3

        with self.cached_session():
            input1 = np.random.rand(samples, timesteps, dim).astype(np.float32)
            layer = keras.layers.Bidirectional(
                rnn(units, return_state=True, return_sequences=True)
            )
            state = layer(input1)[1:]

            input2 = np.random.rand(samples, timesteps, dim).astype(np.float32)
            keras.layers.Bidirectional(rnn(units))(input2, initial_state=state)

    def test_Bidirectional_trainable(self):
        # test layers that need learning_phase to be set
        with self.cached_session():
            x = keras.layers.Input(shape=(3, 2))
            layer = keras.layers.Bidirectional(keras.layers.SimpleRNN(3))
            _ = layer(x)
            assert len(layer.trainable_weights) == 6
            layer.trainable = False
            assert not layer.trainable_weights
            layer.trainable = True
            assert len(layer.trainable_weights) == 6

    def test_Bidirectional_updates(self):
        if tf.executing_eagerly():
            self.skipTest("layer.updates is only available in graph mode.")

        with self.cached_session():
            x = keras.layers.Input(shape=(3, 2))
            x_reachable_update = x * x
            layer = keras.layers.Bidirectional(keras.layers.SimpleRNN(3))
            _ = layer(x)
            assert not layer.updates
            # TODO(b/128684069): Remove when Wrapper sublayers are __call__'d.
            with base_layer_utils.call_context().enter(
                layer, x, {"training": True}, None
            ):
                layer.forward_layer.add_update(x_reachable_update)
                layer.forward_layer.add_update(1)
                layer.backward_layer.add_update(x_reachable_update)
                layer.backward_layer.add_update(1)
            assert len(layer.updates) == 4

    def test_Bidirectional_losses(self):
        x = keras.layers.Input(shape=(3, 2))
        layer = keras.layers.Bidirectional(
            keras.layers.SimpleRNN(
                3,
                kernel_regularizer="l1",
                bias_regularizer="l1",
                activity_regularizer="l1",
            )
        )
        _ = layer(x)
        assert len(layer.losses) == 6

        loss = x * x
        layer.forward_layer.add_loss(loss)
        layer.backward_layer.add_loss(loss)
        assert len(layer.losses) == 8

    def test_Bidirectional_with_constants(self):
        with self.cached_session():
            # Test basic case.
            x = keras.Input((5, 5))
            c = keras.Input((3,))
            cell = _RNNCellWithConstants(32, 3)
            custom_objects = {"_RNNCellWithConstants": _RNNCellWithConstants}
            with keras.utils.CustomObjectScope(custom_objects):
                layer = keras.layers.Bidirectional(keras.layers.RNN(cell))
            y = layer(x, constants=c)
            model = keras.Model([x, c], y)
            model.compile(optimizer="rmsprop", loss="mse")
            model.train_on_batch(
                [np.zeros((6, 5, 5)), np.zeros((6, 3))], np.zeros((6, 64))
            )

            # Test basic case serialization.
            x_np = np.random.random((6, 5, 5))
            c_np = np.random.random((6, 3))
            y_np = model.predict([x_np, c_np])
            weights = model.get_weights()
            config = layer.get_config()

            with keras.utils.CustomObjectScope(custom_objects):
                layer = keras.layers.Bidirectional.from_config(
                    copy.deepcopy(config)
                )
            y = layer(x, constants=c)
            model = keras.Model([x, c], y)
            model.set_weights(weights)
            y_np_2 = model.predict([x_np, c_np])
            self.assertAllClose(y_np, y_np_2, atol=1e-4)

            # Test flat list inputs
            with keras.utils.CustomObjectScope(custom_objects):
                layer = keras.layers.Bidirectional.from_config(
                    copy.deepcopy(config)
                )
            y = layer([x, c])
            model = keras.Model([x, c], y)
            model.set_weights(weights)
            y_np_3 = model.predict([x_np, c_np])
            self.assertAllClose(y_np, y_np_3, atol=1e-4)

    def test_Bidirectional_with_constants_layer_passing_initial_state(self):
        with self.cached_session():
            # Test basic case.
            x = keras.Input((5, 5))
            c = keras.Input((3,))
            s_for = keras.Input((32,))
            s_bac = keras.Input((32,))
            cell = _RNNCellWithConstants(32, 3)
            custom_objects = {"_RNNCellWithConstants": _RNNCellWithConstants}
            with keras.utils.CustomObjectScope(custom_objects):
                layer = keras.layers.Bidirectional(keras.layers.RNN(cell))
            y = layer(x, initial_state=[s_for, s_bac], constants=c)
            model = keras.Model([x, s_for, s_bac, c], y)
            model.compile(optimizer="rmsprop", loss="mse")
            model.train_on_batch(
                [
                    np.zeros((6, 5, 5)),
                    np.zeros((6, 32)),
                    np.zeros((6, 32)),
                    np.zeros((6, 3)),
                ],
                np.zeros((6, 64)),
            )

            # Test basic case serialization.
            x_np = np.random.random((6, 5, 5))
            s_fw_np = np.random.random((6, 32))
            s_bk_np = np.random.random((6, 32))
            c_np = np.random.random((6, 3))
            y_np = model.predict([x_np, s_fw_np, s_bk_np, c_np])
            weights = model.get_weights()
            config = layer.get_config()

            with keras.utils.CustomObjectScope(custom_objects):
                layer = keras.layers.Bidirectional.from_config(
                    copy.deepcopy(config)
                )
            y = layer(x, initial_state=[s_for, s_bac], constants=c)
            model = keras.Model([x, s_for, s_bac, c], y)
            model.set_weights(weights)
            y_np_2 = model.predict([x_np, s_fw_np, s_bk_np, c_np])
            self.assertAllClose(y_np, y_np_2, atol=1e-4)

            # Verify that state is used
            y_np_2_different_s = model.predict(
                [x_np, s_fw_np + 10.0, s_bk_np + 10.0, c_np]
            )
            assert np.mean(y_np - y_np_2_different_s) != 0

            # Test flat list inputs
            with keras.utils.CustomObjectScope(custom_objects):
                layer = keras.layers.Bidirectional.from_config(
                    copy.deepcopy(config)
                )
            y = layer([x, s_for, s_bac, c])
            model = keras.Model([x, s_for, s_bac, c], y)
            model.set_weights(weights)
            y_np_3 = model.predict([x_np, s_fw_np, s_bk_np, c_np])
            self.assertAllClose(y_np, y_np_3, atol=1e-4)

    @parameterized.parameters([keras.layers.LSTM, keras.layers.GRU])
    def test_Bidirectional_output_shape(self, rnn):
        input_shape = [None, 2, 1]
        num_state = 4 if rnn == keras.layers.LSTM else 2

        wrapper = keras.layers.Bidirectional(rnn(3))
        output_shape = wrapper.compute_output_shape(input_shape)
        self.assertEqual(output_shape.as_list(), [None, 6])

        wrapper = keras.layers.Bidirectional(rnn(3, return_state=True))
        output_shape = wrapper.compute_output_shape(input_shape)
        # 1 for output and the rest for forward and backward states
        self.assertLen(output_shape, 1 + num_state)
        self.assertEqual(output_shape[0].as_list(), [None, 6])
        for shape in output_shape[1:]:
            self.assertEqual(shape.as_list(), [None, 3])

        wrapper = keras.layers.Bidirectional(
            rnn(3, return_state=True), merge_mode=None
        )
        output_shape = wrapper.compute_output_shape(input_shape)
        # 1 for forward output and 1 for backward output,  and the rest for
        # states
        self.assertLen(output_shape, 2 + num_state)
        for shape in output_shape:
            self.assertEqual(shape.as_list(), [None, 3])

    def test_Bidirectional_output_shape_return_types(self):
        class TestLayer(keras.layers.SimpleRNN):
            def call(self, inputs):
                return tf.concat([inputs, inputs], axis=-1)

            def compute_output_shape(self, input_shape):
                output_shape = tf.TensorShape(input_shape).as_list()
                output_shape[-1] = output_shape[-1] * 2
                return tf.TensorShape(output_shape)

        class TestListLayer(TestLayer):
            def compute_output_shape(self, input_shape):
                shape = super().compute_output_shape(input_shape)
                return shape.as_list()

        class TestTupleLayer(TestLayer):
            def compute_output_shape(self, input_shape):
                shape = super().compute_output_shape(input_shape)
                return tuple(shape.as_list())

        # Layers can specify output shape as list/tuple/TensorShape
        test_layers = [TestLayer, TestListLayer, TestTupleLayer]
        for layer in test_layers:
            input_layer = keras.layers.Bidirectional(layer(1))
            inputs = keras.backend.placeholder(shape=(None, 2, 4))
            output = input_layer(inputs)
            self.assertEqual(output.shape.as_list(), [None, 2, 16])
            self.assertEqual(
                input_layer.compute_output_shape([None, 2, 4]).as_list(),
                [None, 2, 16],
            )

    @tf.test.disable_with_predicate(
        pred=tf.test.is_built_with_rocm,
        skip_message=(
            "Skipping as ROCm MIOpen does not support padded input yet."
        ),
    )
    def test_Bidirectional_last_output_with_masking(self):
        rnn = keras.layers.LSTM
        samples = 2
        dim = 5
        timesteps = 3
        units = 3
        merge_mode = "concat"
        x = np.random.rand(samples, timesteps, dim)
        # clear the first record's timestep 2. Last output should be same as
        # state, not zeroed.
        x[0, 2] = 0

        with self.cached_session():
            inputs = keras.Input((timesteps, dim))
            masked_inputs = keras.layers.Masking()(inputs)
            wrapped = keras.layers.Bidirectional(
                rnn(units, return_state=True), merge_mode=merge_mode
            )
            outputs = _to_list(wrapped(masked_inputs, training=True))
            self.assertLen(outputs, 5)
            self.assertEqual(outputs[0].shape.as_list(), [None, units * 2])

            model = keras.Model(inputs, outputs)
            y = _to_list(model.predict(x))
            self.assertLen(y, 5)
            self.assertAllClose(y[0], np.concatenate([y[1], y[3]], axis=1))

    @parameterized.parameters([keras.layers.LSTM, keras.layers.GRU])
    @tf.test.disable_with_predicate(
        pred=tf.test.is_built_with_rocm,
        skip_message=(
            "Skipping as ROCm MIOpen does not support padded input yet."
        ),
    )
    def test_Bidirectional_sequence_output_with_masking(self, rnn):
        samples = 2
        dim = 5
        timesteps = 3
        units = 3
        merge_mode = "concat"
        x = np.random.rand(samples, timesteps, dim)
        # clear the first record's timestep 2, and expect the output of timestep
        # 2 is also 0s.
        x[0, 2] = 0

        with self.cached_session():
            inputs = keras.Input((timesteps, dim))
            masked_inputs = keras.layers.Masking()(inputs)
            wrapped = keras.layers.Bidirectional(
                rnn(units, return_sequences=True), merge_mode=merge_mode
            )
            outputs = _to_list(wrapped(masked_inputs, training=True))
            self.assertLen(outputs, 1)
            self.assertEqual(
                outputs[0].shape.as_list(), [None, timesteps, units * 2]
            )

            model = keras.Model(inputs, outputs)
            y = _to_list(model.predict(x))
            self.assertLen(y, 1)
            self.assertAllClose(y[0][0, 2], np.zeros(units * 2))

    @parameterized.parameters(["sum", "concat"])
    def test_custom_backward_layer(self, mode):
        rnn = keras.layers.SimpleRNN
        samples = 2
        dim = 2
        timesteps = 2
        output_dim = 2

        x = np.random.random((samples, timesteps, dim))
        target_dim = 2 * output_dim if mode == "concat" else output_dim
        y = np.random.random((samples, target_dim))
        forward_layer = rnn(output_dim)
        backward_layer = rnn(output_dim, go_backwards=True)

        # test with Sequential model
        model = keras.models.Sequential()
        model.add(
            keras.layers.Bidirectional(
                forward_layer,
                merge_mode=mode,
                backward_layer=backward_layer,
                input_shape=(timesteps, dim),
            )
        )
        model.compile(optimizer="rmsprop", loss="mse")
        model.fit(x, y, epochs=1, batch_size=1)

        # check whether the model variables are present in the
        # trackable list of objects
        checkpointed_object_ids = {
            id(o) for o in trackable_util.list_objects(model)
        }
        for v in model.variables:
            self.assertIn(id(v), checkpointed_object_ids)

        # test compute output shape
        ref_shape = model.layers[-1].output.shape
        shape = model.layers[-1].compute_output_shape((None, timesteps, dim))
        self.assertListEqual(shape.as_list(), ref_shape.as_list())

        # test config
        model.get_config()
        model = keras.models.model_from_json(model.to_json())
        model.summary()

    def test_custom_backward_layer_error_check(self):
        rnn = keras.layers.LSTM
        units = 2

        forward_layer = rnn(units)
        backward_layer = rnn(units)

        with self.assertRaisesRegex(
            ValueError, "should have different `go_backwards` value."
        ):
            keras.layers.Bidirectional(
                forward_layer,
                merge_mode="concat",
                backward_layer=backward_layer,
            )

        for attr in ("stateful", "return_sequences", "return_state"):
            kwargs = {attr: True}
            backward_layer = rnn(units, go_backwards=True, **kwargs)
            with self.assertRaisesRegex(
                ValueError,
                'expected to have the same value for attribute "' + attr,
            ):
                keras.layers.Bidirectional(
                    forward_layer,
                    merge_mode="concat",
                    backward_layer=backward_layer,
                )

    def test_custom_backward_layer_serialization(self):
        rnn = keras.layers.LSTM
        units = 2

        forward_layer = rnn(units)
        backward_layer = rnn(units, go_backwards=True)
        layer = keras.layers.Bidirectional(
            forward_layer, merge_mode="concat", backward_layer=backward_layer
        )
        config = layer.get_config()
        layer_from_config = keras.layers.Bidirectional.from_config(config)
        new_config = layer_from_config.get_config()
        self.assertDictEqual(config, new_config)

    def test_rnn_layer_name(self):
        rnn = keras.layers.LSTM
        units = 2

        layer = keras.layers.Bidirectional(rnn(units, name="rnn"))
        config = layer.get_config()

        self.assertEqual(config["layer"]["config"]["name"], "rnn")

        layer_from_config = keras.layers.Bidirectional.from_config(config)
        self.assertEqual(layer_from_config.forward_layer.name, "forward_rnn")
        self.assertEqual(layer_from_config.backward_layer.name, "backward_rnn")

    def test_custom_backward_rnn_layer_name(self):
        rnn = keras.layers.LSTM
        units = 2

        forward_layer = rnn(units)
        backward_layer = rnn(units, go_backwards=True)
        layer = keras.layers.Bidirectional(
            forward_layer, merge_mode="concat", backward_layer=backward_layer
        )
        config = layer.get_config()

        self.assertEqual(config["layer"]["config"]["name"], "lstm")
        self.assertEqual(config["backward_layer"]["config"]["name"], "lstm_1")

        layer_from_config = keras.layers.Bidirectional.from_config(config)
        self.assertEqual(layer_from_config.forward_layer.name, "forward_lstm")
        self.assertEqual(
            layer_from_config.backward_layer.name, "backward_lstm_1"
        )

    def test_rnn_with_customized_cell(self):
        batch = 20
        dim = 5
        timesteps = 3
        units = 5
        merge_mode = "sum"

        cell = _ResidualLSTMCell(units)
        forward_layer = keras.layers.RNN(cell)
        inputs = keras.Input((timesteps, dim))
        bidirectional_rnn = keras.layers.Bidirectional(
            forward_layer, merge_mode=merge_mode
        )
        outputs = _to_list(bidirectional_rnn(inputs))

        model = keras.Model(inputs, outputs)
        model.compile(optimizer="rmsprop", loss="mse")
        model.fit(
            np.random.random((batch, timesteps, dim)),
            np.random.random((batch, units)),
            epochs=1,
            batch_size=10,
        )

    def test_rnn_with_customized_cell_stacking(self):
        batch = 20
        dim = 5
        timesteps = 3
        units = 5
        merge_mode = "sum"

        cell = [_ResidualLSTMCell(units), _ResidualLSTMCell(units)]
        forward_layer = keras.layers.RNN(cell)
        inputs = keras.Input((timesteps, dim))
        bidirectional_rnn = keras.layers.Bidirectional(
            forward_layer, merge_mode=merge_mode
        )
        outputs = _to_list(bidirectional_rnn(inputs))

        model = keras.Model(inputs, outputs)
        model.compile(optimizer="rmsprop", loss="mse")
        model.fit(
            np.random.random((batch, timesteps, dim)),
            np.random.random((batch, units)),
            epochs=1,
            batch_size=10,
        )

    @test_utils.run_v2_only
    def test_wrapped_rnn_cell(self):
        # See https://github.com/tensorflow/tensorflow/issues/26581.
        batch = 20
        dim = 5
        timesteps = 3
        units = 5
        merge_mode = "sum"

        cell = keras.layers.LSTMCell(units)
        cell = ResidualWrapper(cell)
        rnn = keras.layers.RNN(cell)

        inputs = keras.Input((timesteps, dim))
        wrapped = keras.layers.Bidirectional(rnn, merge_mode=merge_mode)
        outputs = _to_list(wrapped(inputs))

        model = keras.Model(inputs, outputs)
        model.compile(optimizer="rmsprop", loss="mse")
        model.fit(
            np.random.random((batch, timesteps, dim)),
            np.random.random((batch, units)),
            epochs=1,
            batch_size=10,
        )

    @parameterized.parameters(["ave", "concat", "mul"])
    @tf.test.disable_with_predicate(
        pred=tf.test.is_built_with_rocm,
        skip_message=(
            "Skipping as ROCm RNN does not support ragged tensors yet."
        ),
    )
    def test_Bidirectional_ragged_input(self, merge_mode):
        np.random.seed(100)
        rnn = keras.layers.LSTM
        units = 3
        x = tf.ragged.constant(
            [
                [[1, 1, 1], [1, 1, 1]],
                [[1, 1, 1]],
                [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            ],
            ragged_rank=1,
        )
        x = tf.cast(x, "float32")

        with self.cached_session():
            if merge_mode == "ave":
                merge_func = lambda y, y_rev: (y + y_rev) / 2
            elif merge_mode == "concat":
                merge_func = lambda y, y_rev: tf.concat((y, y_rev), axis=-1)
            elif merge_mode == "mul":
                merge_func = lambda y, y_rev: (y * y_rev)

            inputs = keras.Input(
                shape=(None, 3), batch_size=4, dtype="float32", ragged=True
            )
            layer = keras.layers.Bidirectional(
                rnn(units, return_sequences=True), merge_mode=merge_mode
            )
            f_merged = keras.backend.function([inputs], layer(inputs))
            f_forward = keras.backend.function(
                [inputs], layer.forward_layer(inputs)
            )

            # TODO(kaftan): after KerasTensor refactor TF op layers should work
            # with many composite tensors, and this shouldn't need to be a
            # lambda layer.
            reverse_layer = core.Lambda(tf.reverse, arguments=dict(axis=[1]))
            f_backward = keras.backend.function(
                [inputs], reverse_layer(layer.backward_layer(inputs))
            )

            y_merged = f_merged(x)
            y_expected = merge_func(
                convert_ragged_tensor_value(f_forward(x)),
                convert_ragged_tensor_value(f_backward(x)),
            )

            y_merged = convert_ragged_tensor_value(y_merged)
            self.assertAllClose(y_merged.flat_values, y_expected.flat_values)

    def test_Bidirectional_nested_state_reuse(self):
        if not tf.executing_eagerly():
            self.skipTest("Only test eager mode.")
        x = tf.random.normal([4, 8, 16])
        layer = keras.layers.Bidirectional(
            keras.layers.RNN(
                [keras.layers.LSTMCell(5), keras.layers.LSTMCell(5)],
                return_sequences=True,
                return_state=True,
            )
        )
        y = layer(x)
        self.assertAllClose(layer([x] + y[1:]), layer(x, initial_state=y[1:]))

    def test_full_input_spec(self):
        # See https://github.com/tensorflow/tensorflow/issues/38403
        inputs = keras.layers.Input(batch_shape=(1, 1, 1))
        fw_state = keras.layers.Input(batch_shape=(1, 1))
        bw_state = keras.layers.Input(batch_shape=(1, 1))
        states = [fw_state, bw_state]
        bidirectional_rnn = keras.layers.Bidirectional(
            keras.layers.SimpleRNN(1, stateful=True)
        )

        rnn_output = bidirectional_rnn(inputs, initial_state=states)
        model = keras.Model([inputs, fw_state, bw_state], rnn_output)
        output1 = model.predict(
            [np.ones((1, 1, 1)), np.ones((1, 1)), np.ones((1, 1))]
        )
        output2 = model.predict(
            [np.ones((1, 1, 1)), np.ones((1, 1)), np.ones((1, 1))]
        )
        model.reset_states()
        output3 = model.predict(
            [np.ones((1, 1, 1)), np.ones((1, 1)), np.ones((1, 1))]
        )
        self.assertAllClose(output1, output3)
        self.assertNotAllClose(output1, output2)

    def test_reset_states(self):
        ref_state = np.random.rand(1, 3).astype(np.float32)

        # build model
        inp = keras.Input(batch_shape=[1, 2, 3])

        stateful = keras.layers.SimpleRNN(units=3, stateful=True)
        stateless = keras.layers.SimpleRNN(units=3, stateful=False)

        bid_stateless = keras.layers.Bidirectional(stateless)
        bid_stateful = keras.layers.Bidirectional(stateful)

        # required to correctly initialize the state in the layers
        _ = keras.Model(
            inp,
            [
                bid_stateless(inp),
                bid_stateful(inp),
            ],
        )

        with self.assertRaisesRegex(
            AttributeError,
            "Layer must be stateful.",
        ):
            bid_stateless.reset_states()

        with self.assertRaisesRegex(AttributeError, "Layer must be stateful."):
            bid_stateless.reset_states([])

        bid_stateful.reset_states()
        bid_stateful.reset_states([ref_state, ref_state])

        with self.assertRaisesRegex(
            ValueError,
            "Unrecognized value for `states`. Expected `states` "
            "to be list or tuple",
        ):
            bid_stateful.reset_states({})

    def test_trainable_parameter_argument(self):
        inp = keras.layers.Input([None, 3])

        def test(fwd, bwd, **kwargs):
            def _remove_from_dict(d, remove_key):
                if isinstance(d, dict):
                    d.pop(remove_key, None)
                    for key in list(d.keys()):
                        _remove_from_dict(d[key], remove_key)

            bid = keras.layers.Bidirectional(fwd, backward_layer=bwd, **kwargs)

            model = keras.Model(inp, bid(inp))
            clone = keras.models.clone_model(model)

            # Comparison should exclude `build_config`
            clone_config = _remove_from_dict(clone.get_config(), "build_config")
            model_config = _remove_from_dict(model.get_config(), "build_config")
            self.assertEqual(clone_config, model_config)

        # test fetching trainable from `layer`
        fwd = keras.layers.SimpleRNN(units=3)
        bwd = keras.layers.SimpleRNN(units=3, go_backwards=True)

        fwd.trainable = True
        test(fwd, None)

        fwd.trainable = False
        test(fwd, None)

        fwd.trainable = True
        bwd.trainable = False
        test(fwd, bwd)

        fwd.trainable = False
        bwd.trainable = True
        test(fwd, bwd)

        fwd.trainable = True
        bwd.trainable = True
        test(fwd, bwd)

        fwd.trainable = False
        bwd.trainable = False
        test(fwd, bwd)

        # test fetching trainable from `kwargs`
        test(fwd, None, trainable=True)
        test(fwd, None, trainable=False)


def _to_list(ls):
    if isinstance(ls, list):
        return ls
    else:
        return [ls]


def convert_ragged_tensor_value(inputs):
    if isinstance(inputs, tf.compat.v1.ragged.RaggedTensorValue):
        flat_values = tf.convert_to_tensor(
            value=inputs.flat_values, name="flat_values"
        )
        return tf.RaggedTensor.from_nested_row_splits(
            flat_values, inputs.nested_row_splits, validate=False
        )
    return inputs


if __name__ == "__main__":
    tf.test.main()
