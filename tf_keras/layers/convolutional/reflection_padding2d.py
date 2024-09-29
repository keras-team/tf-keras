from base_reflection_padding import BaseReflectionPadding


class ReflectionPadding2D(BaseReflectionPadding):
    """2D reflection padding layer.

    This layer performs reflection padding on a 2D input tensor.
    Inherits from BaseReflectionPadding.

    Args:
        padding: int, or tuple/list of 2 ints, for height and width respectively.
            If int: the same symmetric padding is applied to both dimensions.
            If tuple/list of 2 ints: interpreted as two different symmetric padding values.
    """

    rank = 2

    def __init__(self, padding=(1, 1), **kwargs):
        if isinstance(padding, int):
            padding = (padding, padding)
        super(ReflectionPadding2D, self).__init__(padding=padding, **kwargs)
