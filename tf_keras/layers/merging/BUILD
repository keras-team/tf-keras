# Description:
#  Contains the TF-Keras merging layers.

# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")

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
    deps = [
        ":base_merge",
    ],
)

py_library(
    name = "subtract",
    srcs = ["subtract.py"],
    deps = [
        ":base_merge",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "multiply",
    srcs = ["multiply.py"],
    deps = [
        ":base_merge",
    ],
)

py_library(
    name = "average",
    srcs = ["average.py"],
    deps = [
        ":base_merge",
    ],
)

py_library(
    name = "maximum",
    srcs = ["maximum.py"],
    deps = [
        ":base_merge",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "minimum",
    srcs = ["minimum.py"],
    deps = [
        ":base_merge",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "concatenate",
    srcs = ["concatenate.py"],
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
