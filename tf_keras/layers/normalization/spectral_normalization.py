# Copyright 2023 The TF-Keras Authors. All Rights Reserved.
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

import tensorflow.compat.v2 as tf

from tf_keras.initializers import TruncatedNormal
from tf_keras.layers.rnn import Wrapper

# isort: off
from tensorflow.python.util.tf_export import keras_export


# Adapted from TF-Addons implementation
@keras_export("keras.layers.SpectralNormalization", v1=[])
class SpectralNormalization(Wrapper):
    """Performs spectral normalization on the weights of a target layer.

    This wrapper controls the Lipschitz constant of the weights of a layer by
    constraining their spectral norm, which can stabilize the training of GANs.

    Args:
      layer: A `keras.layers.Layer` instance that
        has either a `kernel` (e.g. `Conv2D`, `Dense`...)
        or an `embeddings` attribute (`Embedding` layer).
      power_iterations: int, the number of iterations during normalization.

    Examples:

    Wrap `keras.layers.Conv2D`:
    >>> x = np.random.rand(1, 10, 10, 1)
    >>> conv2d = SpectralNormalization(tf.keras.layers.Conv2D(2, 2))
    >>> y = conv2d(x)
    >>> y.shape
    TensorShape([1, 9, 9, 2])

    Wrap `keras.layers.Dense`:
    >>> x = np.random.rand(1, 10, 10, 1)
    >>> dense = SpectralNormalization(tf.keras.layers.Dense(10))
    >>> y = dense(x)
    >>> y.shape
    TensorShape([1, 10, 10, 10])

    Reference:

    - [Spectral Normalization for GAN](https://arxiv.org/abs/1802.05957).
    """

    def __init__(self, layer, power_iterations=1, **kwargs):
        super().__init__(layer, **kwargs)
        if power_iterations <= 0:
            raise ValueError(
                "`power_iterations` should be greater than zero. Received: "
                f"`power_iterations={power_iterations}`"
            )
        self.power_iterations = power_iterations

    def build(self, input_shape):
        super().build(input_shape)
        input_shape = tf.TensorShape(input_shape)
        self.input_spec = tf.keras.layers.InputSpec(
            shape=[None] + input_shape[1:]
        )

        if hasattr(self.layer, "kernel"):
            self.kernel = self.layer.kernel
        elif hasattr(self.layer, "embeddings"):
            self.kernel = self.layer.embeddings
        else:
            raise ValueError(
                f"{type(self.layer).__name__} object has no attribute 'kernel' "
                "nor 'embeddings'"
            )

        self.kernel_shape = self.kernel.shape.as_list()

        self.vector_u = self.add_weight(
            shape=(1, self.kernel_shape[-1]),
            initializer=TruncatedNormal(stddev=0.02),
            trainable=False,
            name="vector_u",
            dtype=self.kernel.dtype,
        )

    def call(self, inputs, training=False):
        if training:
            new_vector_u, new_kernel = tf.cond(
                tf.reduce_all(tf.equal(self.kernel.value, 0)),
                lambda: (self.vector_u.value, self.kernel.value),
                self.normalized_weights,
            )
            self.vector_u.assign(new_vector_u)
            self.kernel.assign(new_kernel)

        output = self.layer(inputs)
        return output

    def compute_output_shape(self, input_shape):
        return tf.TensorShape(
            self.layer.compute_output_shape(input_shape).as_list()
        )

    def normalized_weights(self):
        """Generate spectral normalized weights.

        This method returns the updated value for `self.kernel` with the
        spectral normalized value, so that the layer is ready for `call()`.
        """

        weights = tf.reshape(self.kernel, [-1, self.kernel_shape[-1]])
        vector_u = self.vector_u.value

        for _ in range(self.power_iterations):
            vector_v = tf.keras.utils.normalize(
                tf.matmul(vector_u, tf.transpose(weights)), axis=None
            )
            vector_u = tf.keras.utils.normalize(tf.matmul(vector_v, weights), axis=None)
        vector_u = tf.stop_gradient(vector_u)
        vector_v = tf.stop_gradient(vector_v)
        sigma = tf.matmul(
            tf.matmul(vector_v, weights), tf.transpose(vector_u)
        )
        kernel = tf.reshape(tf.divide(self.kernel, sigma), self.kernel_shape)
        return tf.cast(vector_u, self.vector_u.dtype), tf.cast(
            kernel, self.kernel.dtype)

    def get_config(self):
        config = {"power_iterations": self.power_iterations}
        base_config = super().get_config()
        return {**base_config, **config}
