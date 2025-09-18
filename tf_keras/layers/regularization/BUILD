# Description:
#  Contains the TF-Keras regularization layers.

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
    name = "regularization",
    srcs = ["__init__.py"],
    deps = [
        ":activity_regularization",
        ":alpha_dropout",
        ":dropout",
        ":gaussian_dropout",
        ":gaussian_noise",
        ":spatial_dropout1d",
        ":spatial_dropout2d",
        ":spatial_dropout3d",
    ],
)

py_library(
    name = "dropout",
    srcs = ["dropout.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:control_flow_util",
    ],
)

py_library(
    name = "spatial_dropout1d",
    srcs = ["spatial_dropout1d.py"],
    deps = [
        ":dropout",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine:input_spec",
    ],
)

py_library(
    name = "spatial_dropout2d",
    srcs = ["spatial_dropout2d.py"],
    deps = [
        ":dropout",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:input_spec",
    ],
)

py_library(
    name = "spatial_dropout3d",
    srcs = ["spatial_dropout3d.py"],
    deps = [
        ":dropout",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:input_spec",
    ],
)

py_library(
    name = "gaussian_dropout",
    srcs = ["gaussian_dropout.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:tf_utils",
        "@pypi//numpy",
    ],
)

py_library(
    name = "gaussian_noise",
    srcs = ["gaussian_noise.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "activity_regularization",
    srcs = ["activity_regularization.py"],
    deps = [
        "//tf_keras:regularizers",
        "//tf_keras/engine:base_layer",
    ],
)

py_library(
    name = "alpha_dropout",
    srcs = ["alpha_dropout.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:tf_utils",
    ],
)

tf_py_test(
    name = "dropout_test",
    size = "medium",
    srcs = ["dropout_test.py"],
    shard_count = 3,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "spatial_dropout_test",
    size = "medium",
    srcs = ["spatial_dropout_test.py"],
    shard_count = 3,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

tf_py_test(
    name = "gaussian_dropout_test",
    size = "medium",
    srcs = ["gaussian_dropout_test.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "gaussian_noise_test",
    size = "medium",
    srcs = ["gaussian_noise_test.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "activity_regularization_test",
    size = "medium",
    srcs = ["activity_regularization_test.py"],
    shard_count = 3,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "alpha_dropout_test",
    size = "medium",
    srcs = ["alpha_dropout_test.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)
