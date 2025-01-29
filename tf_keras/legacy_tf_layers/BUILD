# Description:
#   Contains the legacy TF layers (internal TensorFlow version).

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")  # buildifier: disable=same-origin-load
# Placeholder: load unaliased py_library

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//learning/brain/contrib:__subpackages__",
        "//tf_keras:friends",
        "//third_party/tensorflow:__subpackages__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "layers",
    srcs = [
        "__init__.py",
    ],
    deps = [
        ":convolutional",
        ":core",
        ":layers_base",
        ":normalization",
        ":pooling",
    ],
)

py_library(
    name = "layers_base",
    srcs = [
        "__init__.py",
        "base.py",
        "migration_utils.py",
        "variable_scope_shim.py",
    ],
    visibility = [
        "//learning/brain/contrib:__subpackages__",
        "//tf_keras:friends",
        "//third_party/tensorflow:__subpackages__",
        "//third_party/tf_seq2seq:__pkg__",
    ],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/mixed_precision:policy",
    ],
)

py_library(
    name = "convolutional",
    srcs = ["convolutional.py"],
    deps = [
        ":layers_base",
        "//:expect_tensorflow_installed",
        "//tf_keras/layers",
    ],
)

py_library(
    name = "core",
    srcs = ["core.py"],
    deps = [
        ":layers_base",
        "//:expect_tensorflow_installed",
        "//tf_keras/layers",
    ],
)

py_library(
    name = "normalization",
    srcs = ["normalization.py"],
    deps = [
        ":layers_base",
        "//:expect_tensorflow_installed",
        "//tf_keras/layers/normalization",
    ],
)

py_library(
    name = "pooling",
    srcs = ["pooling.py"],
    deps = [
        ":layers_base",
        "//:expect_tensorflow_installed",
        "//tf_keras/layers",
    ],
)

tf_py_test(
    name = "base_test",
    size = "small",
    srcs = ["base_test.py"],
    main = "base_test.py",
    deps = [
        ":core",
        ":layers_base",
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "core_test",
    size = "small",
    srcs = ["core_test.py"],
    main = "core_test.py",
    deps = [
        ":core",
        "//:expect_tensorflow_installed",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "convolutional_test",
    size = "small",
    srcs = ["convolutional_test.py"],
    main = "convolutional_test.py",
    deps = [
        ":convolutional",
        "//:expect_tensorflow_installed",
    ],
)

tf_py_test(
    name = "pooling_test",
    size = "small",
    srcs = ["pooling_test.py"],
    main = "pooling_test.py",
    tags = ["no_rocm"],
    deps = [
        ":pooling",
        "//:expect_tensorflow_installed",
    ],
)

cuda_py_test(
    name = "normalization_test",
    size = "medium",
    srcs = ["normalization_test.py"],
    main = "normalization_test.py",
    shard_count = 10,
    deps = [
        ":convolutional",
        ":layers_base",
        ":normalization",
        "//:expect_tensorflow_installed",
    ],
)

tf_py_test(
    name = "variable_scope_shim_test",
    size = "small",
    srcs = ["variable_scope_shim_test.py"],
    main = "variable_scope_shim_test.py",
    tags = ["no_windows"],
    deps = [
        ":core",
        ":layers_base",
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "migration_utils_test",
    size = "small",
    srcs = ["migration_utils_test.py"],
    main = "migration_utils_test.py",
    deps = [
        ":layers",
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/testing_infra:test_combinations",
    ],
)
