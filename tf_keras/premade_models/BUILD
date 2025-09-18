# Description:
#   Contains the TF-Keras Premade Models (internal TensorFlow version).
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
    name = "premade_models",
    srcs = [
        "__init__.py",
        "linear.py",
        "wide_deep.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend_config",
        "//tf_keras:regularizers",
    ],
)

tf_py_test(
    name = "linear_test",
    size = "medium",
    srcs = ["linear_test.py"],
    shard_count = 2,
    deps = [
        ":premade_models",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "wide_deep_test",
    size = "medium",
    srcs = ["wide_deep_test.py"],
    shard_count = 2,
    deps = [
        ":premade_models",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)
