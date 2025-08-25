# Description:
#  Contains the TF-Keras convolution layers.

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")
# Placeholder: load unaliased py_library

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = ["//tf_keras:__subpackages__"],
    licenses = ["notice"],
)

py_library(
    name = "convolutional",
    srcs = [
        "__init__.py",
    ],
    deps = [
        ":conv1d",
        ":conv1d_transpose",
        ":conv2d",
        ":conv2d_transpose",
        ":conv3d",
        ":conv3d_transpose",
        ":depthwise_conv1d",
        ":depthwise_conv2d",
        ":separable_conv1d",
        ":separable_conv2d",
        "//tf_keras/layers/pooling:average_pooling1d",
        "//tf_keras/layers/pooling:average_pooling2d",
        "//tf_keras/layers/pooling:average_pooling3d",
        "//tf_keras/layers/pooling:max_pooling1d",
        "//tf_keras/layers/pooling:max_pooling2d",
        "//tf_keras/layers/pooling:max_pooling3d",
        "//tf_keras/layers/reshaping:cropping1d",
        "//tf_keras/layers/reshaping:cropping2d",
        "//tf_keras/layers/reshaping:cropping3d",
        "//tf_keras/layers/reshaping:up_sampling1d",
        "//tf_keras/layers/reshaping:up_sampling2d",
        "//tf_keras/layers/reshaping:up_sampling3d",
        "//tf_keras/layers/reshaping:zero_padding1d",
        "//tf_keras/layers/reshaping:zero_padding2d",
        "//tf_keras/layers/reshaping:zero_padding3d",
    ],
)

py_library(
    name = "base_conv",
    srcs = ["base_conv.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "conv1d",
    srcs = ["conv1d.py"],
    deps = [
        ":base_conv",
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/dtensor:utils",
        "//tf_keras/initializers",
    ],
)

py_library(
    name = "conv2d",
    srcs = ["conv2d.py"],
    deps = [
        ":base_conv",
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/dtensor:utils",
        "//tf_keras/initializers",
    ],
)

py_library(
    name = "conv3d",
    srcs = ["conv3d.py"],
    deps = [
        ":base_conv",
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/dtensor:utils",
        "//tf_keras/initializers",
    ],
)

py_library(
    name = "conv1d_transpose",
    srcs = ["conv1d_transpose.py"],
    deps = [
        ":conv1d",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/dtensor:utils",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "conv2d_transpose",
    srcs = ["conv2d_transpose.py"],
    deps = [
        ":conv2d",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:activations",
        "//tf_keras:backend",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/dtensor:utils",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "conv3d_transpose",
    srcs = ["conv3d_transpose.py"],
    deps = [
        ":conv3d",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/dtensor:utils",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "base_separable_conv",
    srcs = ["base_separable_conv.py"],
    deps = [
        ":base_conv",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
    ],
)

py_library(
    name = "separable_conv1d",
    srcs = ["separable_conv1d.py"],
    deps = [
        ":base_separable_conv",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/initializers",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "separable_conv2d",
    srcs = ["separable_conv2d.py"],
    deps = [
        ":base_separable_conv",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/initializers",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "base_depthwise_conv",
    srcs = ["base_depthwise_conv.py"],
    deps = [
        ":base_conv",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
    ],
)

py_library(
    name = "depthwise_conv1d",
    srcs = ["depthwise_conv1d.py"],
    deps = [
        ":base_depthwise_conv",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "depthwise_conv2d",
    srcs = ["depthwise_conv2d.py"],
    deps = [
        ":base_depthwise_conv",
        "//tf_keras:backend",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

cuda_py_test(
    name = "conv_test",
    size = "medium",
    srcs = ["conv_test.py"],
    shard_count = 8,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

cuda_py_test(
    name = "conv_transpose_test",
    size = "medium",
    srcs = ["conv_transpose_test.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

cuda_py_test(
    name = "depthwise_conv_test",
    size = "medium",
    srcs = ["depthwise_conv_test.py"],
    shard_count = 8,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

cuda_py_test(
    name = "separable_conv_test",
    size = "medium",
    srcs = ["separable_conv_test.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)
