# Description:
#  Contains the TF-Keras reshaping layers.

# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")

# buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:__subpackages__",
        "//third_party/tensorflow/python/distribute:__pkg__",
        "//third_party/tensorflow/python/feature_column:__pkg__",
        "//third_party/tensorflow/python/trackable:__pkg__",
        "//third_party/tensorflow/tools/pip_package:__pkg__",
        "//third_party/tensorflow_models/official/projects/residual_mobilenet/modeling/backbones:__pkg__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "reshaping",
    srcs = [
        "__init__.py",
    ],
    deps = [
        ":cropping1d",
        ":cropping2d",
        ":cropping3d",
        ":flatten",
        ":permute",
        ":repeat_vector",
        ":reshape",
        ":up_sampling1d",
        ":up_sampling2d",
        ":up_sampling3d",
        ":zero_padding1d",
        ":zero_padding2d",
        ":zero_padding3d",
    ],
)

py_library(
    name = "cropping1d",
    srcs = ["cropping1d.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "cropping2d",
    srcs = ["cropping2d.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "cropping3d",
    srcs = ["cropping3d.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "flatten",
    srcs = ["flatten.py"],
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "permute",
    srcs = ["permute.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
    ],
)

py_library(
    name = "repeat_vector",
    srcs = ["repeat_vector.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
    ],
)

py_library(
    name = "reshape",
    srcs = ["reshape.py"],
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
    ],
)

py_library(
    name = "up_sampling1d",
    srcs = ["up_sampling1d.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
    ],
)

py_library(
    name = "up_sampling2d",
    srcs = ["up_sampling2d.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "up_sampling3d",
    srcs = ["up_sampling3d.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "zero_padding1d",
    srcs = ["zero_padding1d.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "zero_padding2d",
    srcs = ["zero_padding2d.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "zero_padding3d",
    srcs = ["zero_padding3d.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

cuda_py_test(
    name = "cropping_test",
    size = "medium",
    srcs = ["cropping_test.py"],
    shard_count = 8,
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

tf_py_test(
    name = "flatten_test",
    size = "medium",
    srcs = ["flatten_test.py"],
    shard_count = 3,
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "permute_test",
    size = "medium",
    srcs = ["permute_test.py"],
    shard_count = 3,
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "repeat_vector_test",
    size = "medium",
    srcs = ["repeat_vector_test.py"],
    shard_count = 3,
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "reshape_test",
    size = "medium",
    srcs = ["reshape_test.py"],
    shard_count = 3,
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "up_sampling_test",
    size = "medium",
    srcs = ["up_sampling_test.py"],
    shard_count = 8,
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

cuda_py_test(
    name = "zero_padding_test",
    size = "medium",
    srcs = ["zero_padding_test.py"],
    shard_count = 8,
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)
