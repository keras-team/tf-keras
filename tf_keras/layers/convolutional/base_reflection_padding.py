import tensorflow as tf
from tensorflow.keras.layers import Layer


class BaseReflectionPadding(Layer):
    """Abstract N-D reflection padding layer.

    This layer performs reflection padding on the input tensor.

    Args:
        padding: int, or tuple/list of n ints, for n > 1.
            If int: the same symmetric padding is applied to all spatial dimensions.
            If tuple/list of n ints: interpreted as n different symmetric padding values
            for each spatial dimension. 
            No padding is applied to the batch or channel dimensions.

    Raises:
        ValueError: If `padding` is negative or not of length 2 or more.

    """

    def __init__(self, padding=(1, 1), **kwargs):
        super(BaseReflectionPadding, self).__init__(**kwargs)
        if isinstance(padding, int):
            self.padding = (padding, padding)
        elif isinstance(padding, tuple) or isinstance(padding, list):
            if len(padding) != self.rank:
                raise ValueError(
                    f"If passing a tuple or list as padding, it must be of length {self.rank}. Received length: {len(padding)}"
                )
            self.padding = padding
        else:
            raise ValueError(
                f"Unsupported padding type. Expected int, tuple, or list. Received: {type(padding)}"
            )

        for pad in self.padding:
            if pad < 0:
                raise ValueError("Padding cannot be negative.")

    def compute_output_shape(self, input_shape):
        output_shape = list(input_shape)
        for i in range(1, self.rank + 1):
            output_shape[i] += 2 * self.padding[i - 1]
        return tuple(output_shape)

    def call(self, inputs):
        padding_dims = [[0, 0]]
        for pad in self.padding:
            padding_dims.append([pad, pad])
        for _ in range(self.rank - len(self.padding)):
            padding_dims.append([0, 0])
        return tf.pad(inputs, padding_dims, mode='REFLECT')
