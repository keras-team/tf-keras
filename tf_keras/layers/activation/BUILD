# Description:
#  Contains the TF-Keras activation layers.

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
    name = "activation",
    srcs = [
        "__init__.py",
    ],
    srcs_version = "PY3",
    deps = [
        ":elu",
        ":leaky_relu",
        ":prelu",
        ":relu",
        ":softmax",
        ":thresholded_relu",
    ],
)

py_library(
    name = "relu",
    srcs = ["relu.py"],
    srcs_version = "PY3",
    deps = [
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "softmax",
    srcs = ["softmax.py"],
    srcs_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "leaky_relu",
    srcs = ["leaky_relu.py"],
    srcs_version = "PY3",
    deps = [
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "prelu",
    srcs = ["prelu.py"],
    srcs_version = "PY3",
    deps = [
        "//tf_keras:backend",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "elu",
    srcs = ["elu.py"],
    srcs_version = "PY3",
    deps = [
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "thresholded_relu",
    srcs = ["thresholded_relu.py"],
    srcs_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:tf_utils",
    ],
)

tf_py_test(
    name = "relu_test",
    size = "medium",
    srcs = ["relu_test.py"],
    python_version = "PY3",
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

tf_py_test(
    name = "softmax_test",
    size = "medium",
    srcs = ["softmax_test.py"],
    python_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

tf_py_test(
    name = "leaky_relu_test",
    size = "medium",
    srcs = ["leaky_relu_test.py"],
    python_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

tf_py_test(
    name = "prelu_test",
    size = "medium",
    srcs = ["prelu_test.py"],
    python_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

tf_py_test(
    name = "elu_test",
    size = "medium",
    srcs = ["elu_test.py"],
    python_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

tf_py_test(
    name = "thresholded_relu_test",
    size = "medium",
    srcs = ["thresholded_relu_test.py"],
    python_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)
