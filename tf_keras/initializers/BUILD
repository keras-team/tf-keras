# Description:
#   Contains the TF-Keras initializer API (internal TensorFlow version).

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
load("@rules_python//python:py_library.bzl", "py_library")

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
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
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
    deps = [
        ":initializers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine",
        "//tf_keras/models",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)
