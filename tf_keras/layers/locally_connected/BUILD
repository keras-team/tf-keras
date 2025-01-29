# Description:
#  Contains the TF-Keras locally-connected layers.

# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
    ],
    licenses = ["notice"],
)

py_library(
    name = "locally_connected",
    srcs = [
        "__init__.py",
    ],
    deps = [
        ":locally_connected1d",
        ":locally_connected2d",
    ],
)

py_library(
    name = "locally_connected_utils",
    srcs = ["locally_connected_utils.py"],
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "locally_connected1d",
    srcs = ["locally_connected1d.py"],
    deps = [
        ":locally_connected_utils",
        "//tf_keras:activations",
        "//tf_keras:backend",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "locally_connected2d",
    srcs = ["locally_connected2d.py"],
    deps = [
        ":locally_connected_utils",
        "//tf_keras:activations",
        "//tf_keras:backend",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

tf_py_test(
    name = "locally_connected_test",
    size = "medium",
    srcs = ["locally_connected_test.py"],
    shard_count = 4,
    tags = ["no_windows"],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)
