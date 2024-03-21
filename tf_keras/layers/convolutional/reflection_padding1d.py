from base_reflection_padding import BaseReflectionPadding


class ReflectionPadding1D(BaseReflectionPadding):
    """1D reflection padding layer.

    This layer performs reflection padding on a 1D input tensor.
    Inherits from BaseReflectionPadding.

    Args:
        padding: int, or tuple/list of 1 int, specifying the padding width.
            If int: the same symmetric padding is applied to both sides.
            If tuple/list of 1 int: interpreted as two different symmetric padding values.
    """

    rank = 1

    def __init__(self, padding=1, **kwargs):
        super(ReflectionPadding1D, self).__init__(
            padding=(padding,), **kwargs)
