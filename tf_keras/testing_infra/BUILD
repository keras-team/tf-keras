# Description:
#   Contains the TF-Keras testing infrastructure.

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
# Placeholder: load unaliased py_library

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
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

py_library(
    name = "test_utils",
    srcs = [
        "__init__.py",
        "test_utils.py",
    ],
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
        ":keras_doctest_lib",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "@pypi//absl_py",  # absl/testing:parameterized
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
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)
