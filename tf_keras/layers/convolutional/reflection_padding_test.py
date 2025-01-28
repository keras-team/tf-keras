import numpy as np
import tensorflow as tf
from absl.testing import parameterized
from reflection_padding1d import ReflectionPadding1D
from reflection_padding2d import ReflectionPadding2D
from reflection_padding3d import ReflectionPadding3D

from tf_keras.testing_infra import test_combinations
from tf_keras.testing_infra import test_utils


@test_combinations.run_all_keras_modes
class ReflectionPaddingTest(test_combinations.TestCase):
    def _run_test(self, padding_layer_cls, kwargs, input_shape, expected_output_shape):
        with self.cached_session():
            test_utils.layer_test(
                padding_layer_cls,
                kwargs=kwargs,
                input_shape=input_shape,
                expected_output_shape=expected_output_shape,
            )

    @parameterized.named_parameters(
        ("ReflectionPadding1D", ReflectionPadding1D,
         {"padding": 2}, (None, 5, 3), (None, 9, 3)),
        ("ReflectionPadding2D", ReflectionPadding2D, {
         "padding": (2, 1)}, (None, 5, 6, 3), (None, 9, 8, 3)),
        ("ReflectionPadding3D", ReflectionPadding3D, {
         "padding": (1, 2, 3)}, (None, 5, 6, 7, 3), (None, 7, 10, 13, 3)),
    )
    def test_reflection_padding(self, padding_layer_cls, kwargs, input_shape, expected_output_shape):
        self._run_test(padding_layer_cls, kwargs,
                       input_shape, expected_output_shape)

    def test_reflection_padding_dynamic_shape(self):
        with self.cached_session():
            layer = ReflectionPadding2D(padding=(2, 2))
            input_shape = (None, None, None, 3)
            inputs = tf.keras.Input(shape=input_shape)
            x = layer(inputs)
            # Won't raise error here with None values in input shape.
            layer(x)


if __name__ == "__main__":
    tf.test.main()
