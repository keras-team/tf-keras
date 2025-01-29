# Description:
#   Contains the TF-Keras testing infrastructure.

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
# Placeholder: load unaliased py_library
# Placeholder: load unaliased py_test

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = ["//tf_keras:friends"],
    licenses = ["notice"],
)

py_library(
    name = "test_combinations",
    srcs = [
        "test_combinations.py",
    ],
    deps = [
        ":test_utils",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
    ],
)

py_library(
    name = "test_utils",
    srcs = [
        "test_utils.py",
    ],
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer_utils",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/utils:tf_contextlib",
        "//tf_keras/utils:tf_inspect",
    ],
)

# TODO(mattdangerw): For now, TF-Keras will maintain its own doc checker.
# If TensorFlow exposes one, we could consider depending on that directly.
py_library(
    name = "keras_doctest_lib",
    srcs = ["keras_doctest_lib.py"],
    deps = [
        "//:expect_numpy_installed",
    ],
)

py_test(
    name = "keras_doctest_lib_test",
    srcs = ["keras_doctest_lib_test.py"],
    tags = [
        "noasan",
        "nomsan",
        "notsan",
    ],
    deps = [
        ":keras_doctest_lib",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
    ],
)

tf_py_test(
    name = "test_combinations_test",
    size = "small",
    srcs = ["test_combinations_test.py"],
    tags = ["notsan"],
    deps = [
        ":test_combinations",
        ":test_utils",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
    ],
)
