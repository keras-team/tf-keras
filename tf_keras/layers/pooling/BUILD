# Description:
#  Contains the TF-Keras pooling layers.

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
    name = "pooling",
    srcs = ["__init__.py"],
    strict_deps = False,
    deps = [
        ":average_pooling1d",
        ":average_pooling2d",
        ":average_pooling3d",
        ":global_average_pooling1d",
        ":global_average_pooling2d",
        ":global_average_pooling3d",
        ":global_max_pooling1d",
        ":global_max_pooling2d",
        ":global_max_pooling3d",
        ":max_pooling1d",
        ":max_pooling2d",
        ":max_pooling3d",
    ],
)

py_library(
    name = "base_pooling1d",
    srcs = ["base_pooling1d.py"],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "base_pooling2d",
    srcs = ["base_pooling2d.py"],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "base_pooling3d",
    srcs = ["base_pooling3d.py"],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "base_global_pooling1d",
    srcs = ["base_global_pooling1d.py"],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "base_global_pooling2d",
    srcs = ["base_global_pooling2d.py"],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "base_global_pooling3d",
    srcs = ["base_global_pooling3d.py"],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "max_pooling1d",
    srcs = ["max_pooling1d.py"],
    strict_deps = False,
    deps = [
        ":base_pooling1d",
        "//tf_keras:backend",
    ],
)

py_library(
    name = "max_pooling2d",
    srcs = ["max_pooling2d.py"],
    strict_deps = False,
    deps = [
        ":base_pooling2d",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "max_pooling3d",
    srcs = ["max_pooling3d.py"],
    strict_deps = False,
    deps = [
        ":base_pooling3d",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "average_pooling1d",
    srcs = ["average_pooling1d.py"],
    strict_deps = False,
    deps = [
        ":base_pooling1d",
        "//tf_keras:backend",
    ],
)

py_library(
    name = "average_pooling2d",
    srcs = ["average_pooling2d.py"],
    strict_deps = False,
    deps = [
        ":base_pooling2d",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "average_pooling3d",
    srcs = ["average_pooling3d.py"],
    strict_deps = False,
    deps = [
        ":base_pooling3d",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "global_max_pooling1d",
    srcs = ["global_max_pooling1d.py"],
    strict_deps = False,
    deps = [
        ":base_global_pooling1d",
        "//tf_keras:backend",
    ],
)

py_library(
    name = "global_max_pooling2d",
    srcs = ["global_max_pooling2d.py"],
    strict_deps = False,
    deps = [
        ":base_global_pooling2d",
        "//tf_keras:backend",
    ],
)

py_library(
    name = "global_max_pooling3d",
    srcs = ["global_max_pooling3d.py"],
    strict_deps = False,
    deps = [
        ":base_global_pooling3d",
        "//tf_keras:backend",
    ],
)

py_library(
    name = "global_average_pooling1d",
    srcs = ["global_average_pooling1d.py"],
    strict_deps = False,
    deps = [
        ":base_global_pooling1d",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
    ],
)

py_library(
    name = "global_average_pooling2d",
    srcs = ["global_average_pooling2d.py"],
    strict_deps = False,
    deps = [
        ":base_global_pooling2d",
        "//tf_keras:backend",
    ],
)

py_library(
    name = "global_average_pooling3d",
    srcs = ["global_average_pooling3d.py"],
    strict_deps = False,
    deps = [
        ":base_global_pooling3d",
        "//tf_keras:backend",
    ],
)

tf_py_test(
    name = "average_pooling_test",
    size = "medium",
    srcs = ["average_pooling_test.py"],
    shard_count = 8,
    tags = [
        "notsan",  # TODO(b/183962355)
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

tf_py_test(
    name = "max_pooling_test",
    size = "medium",
    srcs = ["max_pooling_test.py"],
    shard_count = 8,
    tags = [
        "notsan",  # TODO(b/183962355)
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

tf_py_test(
    name = "global_average_pooling_test",
    size = "medium",
    srcs = ["global_average_pooling_test.py"],
    shard_count = 8,
    tags = [
        "notsan",  # TODO(b/183962355)
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

tf_py_test(
    name = "global_max_pooling_test",
    size = "medium",
    srcs = ["global_max_pooling_test.py"],
    shard_count = 8,
    tags = [
        "notsan",  # TODO(b/183962355)
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)
