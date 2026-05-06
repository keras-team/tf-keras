# Description:
#   Contains the TF-Keras testing infrastructure.

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
load("@rules_python//python:py_library.bzl", "py_library")

package(
    default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = ["//tf_keras:friends"],
    licenses = ["notice"],
)

py_library(
    name = "test_combinations",
    srcs = [
        "test_combinations.py",
    ],
    strict_deps = False,
    deps = [
        "# //third_party/py/absl/testing:parameterized",
        ":test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
    ],
)

py_library(
    name = "test_utils",
    srcs = [
        "__init__.py",
        "test_utils.py",
    ],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer_utils",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/utils:tf_contextlib",
        "//tf_keras/utils:tf_inspect",
        "@pypi//numpy",
    ],
)

# TODO(mattdangerw): For now, TF-Keras will maintain its own doc checker.
# If TensorFlow exposes one, we could consider depending on that directly.
py_library(
    name = "keras_doctest_lib",
    srcs = ["keras_doctest_lib.py"],
    strict_deps = False,
    deps = [
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "keras_doctest_lib_test",
    srcs = ["keras_doctest_lib_test.py"],
    tags = [
        "noasan",
        "nomsan",
        "notsan",
    ],
    deps = [
        "# //third_party/py/absl/testing:parameterized",
        ":keras_doctest_lib",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

tf_py_test(
    name = "test_combinations_test",
    size = "small",
    srcs = ["test_combinations_test.py"],
    tags = ["notsan"],
    deps = [
        "# //third_party/py/absl/testing:parameterized",
        ":test_combinations",
        ":test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "@pypi//numpy",
    ],
)
