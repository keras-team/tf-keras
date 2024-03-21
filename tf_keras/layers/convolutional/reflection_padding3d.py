from base_reflection_padding import BaseReflectionPadding


class ReflectionPadding3D(BaseReflectionPadding):
    """3D reflection padding layer.

    This layer performs reflection padding on a 3D input tensor.
    Inherits from BaseReflectionPadding.

    Args:
        padding: int, or tuple/list of 3 ints, for height, width, and depth respectively.
            If int: the same symmetric padding is applied to all dimensions.
            If tuple/list of 3 ints: interpreted as three different symmetric padding values.
    """

    rank = 3

    def __init__(self, padding=(1, 1, 1), **kwargs):
        if isinstance(padding, int) and padding > 0:
            padding = (padding, padding, padding)
        super(ReflectionPadding3D, self).__init__(padding=padding, **kwargs)
