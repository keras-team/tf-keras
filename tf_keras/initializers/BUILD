# Description:
#   Contains the TF-Keras initializer API (internal TensorFlow version).

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
    name = "initializers",
    srcs = [
        "__init__.py",
        "initializers.py",
        "initializers_v1.py",
    ],
    srcs_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/dtensor:utils",
        "//tf_keras/saving:serialization_lib",
        "//tf_keras/utils:generic_utils",
        "//tf_keras/utils:tf_inspect",
    ],
)

tf_py_test(
    name = "initializers_test",
    size = "small",
    srcs = ["initializers_test.py"],
    python_version = "PY3",
    deps = [
        ":initializers",
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine",
        "//tf_keras/models",
        "//tf_keras/testing_infra:test_combinations",
    ],
)
