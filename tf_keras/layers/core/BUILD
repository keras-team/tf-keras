# Placeholder: load unaliased py_library

# Description:
#  Contains the TF-Keras core layers.
load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")

# buildifier: disable=same-origin-load
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
    name = "core",
    srcs = [
        "__init__.py",
    ],
    deps = [
        ":activation",
        ":dense",
        ":einsum_dense",
        ":embedding",
        ":identity",
        ":lambda",
        ":masking",
        ":tf_op_layer",
        "//tf_keras/layers/regularization:activity_regularization",
        "//tf_keras/layers/regularization:dropout",
        "//tf_keras/layers/regularization:spatial_dropout1d",
        "//tf_keras/layers/regularization:spatial_dropout2d",
        "//tf_keras/layers/regularization:spatial_dropout3d",
        "//tf_keras/layers/reshaping:flatten",
        "//tf_keras/layers/reshaping:permute",
        "//tf_keras/layers/reshaping:repeat_vector",
        "//tf_keras/layers/reshaping:reshape",
    ],
)

py_library(
    name = "activation",
    srcs = ["activation.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
    ],
)

py_library(
    name = "dense",
    srcs = ["dense.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/dtensor:utils",
    ],
)

py_library(
    name = "einsum_dense",
    srcs = ["einsum_dense.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:activations",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/engine:base_layer",
        "//tf_keras/initializers",
    ],
)

py_library(
    name = "embedding",
    srcs = ["embedding.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/dtensor:utils",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:base_layer_utils",
        "//tf_keras/initializers",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "lambda",
    srcs = ["lambda_layer.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
    ],
)

py_library(
    name = "masking",
    srcs = ["masking.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
    ],
)

py_library(
    name = "tf_op_layer",
    srcs = ["tf_op_layer.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras:constraints",
        "//tf_keras:regularizers",
        "//tf_keras/engine:base_layer",
        "//tf_keras/initializers",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "identity",
    srcs = ["identity.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine:base_layer",
    ],
)

tf_py_test(
    name = "core_test",
    size = "medium",
    srcs = ["core_test.py"],
    shard_count = 3,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "einsum_dense_test",
    srcs = ["einsum_dense_test.py"],
    deps = [
        ":einsum_dense",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

cuda_py_test(
    name = "embedding_test",
    size = "medium",
    srcs = ["embedding_test.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/mixed_precision:policy",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)
