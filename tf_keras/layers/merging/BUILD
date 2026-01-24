# Description:
#  Contains the TF-Keras merging layers.

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
load("@rules_python//python:py_library.bzl", "py_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/py/tensorflow_gnn:__subpackages__",
        "//third_party/tensorflow/python/distribute:__pkg__",
        "//third_party/tensorflow/python/feature_column:__pkg__",
        "//third_party/tensorflow/python/trackable:__pkg__",
        "//third_party/tensorflow/tools/pip_package:__pkg__",
        "//third_party/tensorflow_models/official/projects/residual_mobilenet/modeling/backbones:__pkg__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "merging",
    srcs = ["__init__.py"],
    strict_deps = False,
    deps = [
        ":add",
        ":average",
        ":concatenate",
        ":dot",
        ":maximum",
        ":minimum",
        ":multiply",
        ":subtract",
    ],
)

py_library(
    name = "base_merge",
    srcs = ["base_merge.py"],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "add",
    srcs = ["add.py"],
    strict_deps = False,
    deps = [
        ":base_merge",
    ],
)

py_library(
    name = "subtract",
    srcs = ["subtract.py"],
    strict_deps = False,
    deps = [
        ":base_merge",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "multiply",
    srcs = ["multiply.py"],
    strict_deps = False,
    deps = [
        ":base_merge",
    ],
)

py_library(
    name = "average",
    srcs = ["average.py"],
    strict_deps = False,
    deps = [
        ":base_merge",
    ],
)

py_library(
    name = "maximum",
    srcs = ["maximum.py"],
    strict_deps = False,
    deps = [
        ":base_merge",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "minimum",
    srcs = ["minimum.py"],
    strict_deps = False,
    deps = [
        ":base_merge",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "concatenate",
    srcs = ["concatenate.py"],
    strict_deps = False,
    deps = [
        ":base_merge",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "dot",
    srcs = ["dot.py"],
    strict_deps = False,
    deps = [
        ":base_merge",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

tf_py_test(
    name = "merging_test",
    size = "medium",
    srcs = ["merging_test.py"],
    shard_count = 4,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)
