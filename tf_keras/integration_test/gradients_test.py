# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
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

import numpy as np
import tensorflow.compat.v2 as tf

import tf_keras as keras


class TestKerasModelClass(keras.Model):
    """A simple tensorflow keras Model class definition."""

    def __init__(self, width):
        super().__init__()
        self.width = width

    def build(self, input_shape):
        self.weight = self.add_weight(
            name="test_keras_var",
            shape=(self.width,),
            dtype=tf.float32,
            trainable=True,
        )

    def call(self, inputs):
        return self.weight * inputs


class GradientsTest(tf.test.TestCase):
    def _TestVariablesGradient(self, inputs, test_model, vars_to_grad):
        """Returns gradients of `test_model` with respect to `vars_to_grad`."""

        test_model_re = tf.recompute_grad(test_model)

        with tf.GradientTape(persistent=True) as tape:
            tape.watch(vars_to_grad)
            out_re = test_model_re(inputs)
            out = test_model(inputs)

        grads_re = tape.gradient(out_re, vars_to_grad)
        grads = tape.gradient(out, vars_to_grad)

        return grads_re, grads

    def testKerasRecompute(self):
        """Checks that recompute_grad works for a simple TF-Keras Model."""

        test_model = TestKerasModelClass(10)
        test_input = tf.constant(tf.zeros((10, 10), dtype=np.float32))
        # Ensures keras model is initialized.
        test_model(test_input)
        grads_re, grads = self._TestVariablesGradient(
            test_input, test_model, test_input
        )

        grads_re = self.evaluate(grads_re)
        grads = self.evaluate(grads)
        for g, g_re in zip(grads, grads_re):
            self.assertAllClose(g, g_re)

        grads_re, grads = self._TestVariablesGradient(
            test_input, test_model, test_model.variables
        )

        grads_re = self.evaluate(grads_re)
        grads = self.evaluate(grads)
        for g, g_re in zip(grads, grads_re):
            self.assertAllClose(g, g_re)

    def testLSTMBatchJacobian(self):
        class HasLSTM(keras.Model):
            def __init__(self):
                super().__init__()
                self.lstm = keras.layers.LSTM(units=5)
                self.dense = keras.layers.Dense(1, activation=tf.nn.sigmoid)

            def call(self, x):
                return self.dense(self.lstm(x))

        m = HasLSTM()

        def jacobian(x):
            with tf.GradientTape() as tape:
                tape.watch(x)
                y = m(x)
            return tape.batch_jacobian(y, x)

        inp = tf.nn.l2_normalize(tf.ones([1, 2, 3]), axis=[1, 2])
        eager_result = jacobian(inp)
        function_result = tf.function(jacobian)(inp)
        self.assertAllClose(eager_result, function_result)
        backprop_result, numeric_result = tf.test.compute_gradient(
            m, [inp], delta=1e-3
        )
        self.assertAllClose(numeric_result, backprop_result, atol=1e-3)
        self.assertAllClose(
            tf.reshape(numeric_result, [-1]),
            tf.reshape(eager_result, [-1]),
            atol=1e-3,
        )

    def testEmbeddingLookupGradientsHaveKnownShape(self):
        class MyLayer(keras.layers.Layer):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.embedding = None

            def build(self, input_shape):
                self.embedding = tf.Variable(tf.random.uniform([50, 16]))

            def call(self, x):
                return tf.nn.embedding_lookup(self.embedding, x)

        layer = MyLayer()

        @tf.function
        def _run(x):
            with tf.GradientTape() as tape:
                y = layer(x)
                loss = tf.math.reduce_sum(y)
            gradients = tape.gradient(loss, layer.weights)
            self.assertListEqual(gradients[0].shape.as_list(), [50, 16])

        _run(tf.random.uniform([4, 16], minval=0, maxval=50, dtype=tf.int64))


if __name__ == "__main__":
    if tf.__internal__.tf2.enabled():
        tf.test.main()
