# Description:
#   Contains the TF-Keras layers (internal TensorFlow version).

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
# Placeholder: load unaliased py_library

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    # TODO(scottzhu): Remove non-keras deps from TF.
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/python/distribute:__pkg__",
        "//third_party/tensorflow/python/feature_column:__pkg__",
        "//third_party/tensorflow/python/trackable:__pkg__",
        "//third_party/tensorflow/tools/pip_package:__pkg__",
    ],
    licenses = ["notice"],
)

# A separate build for layers without serialization to avoid circular deps
# with feature column.
py_library(
    name = "layers",
    srcs = [
        "__init__.py",
        "serialization.py",
    ],
    deps = [
        ":kernelized",
        ":noise",
        "//tf_keras/feature_column",
        "//tf_keras/layers/activation",
        "//tf_keras/layers/attention",
        "//tf_keras/layers/convolutional",
        "//tf_keras/layers/core",
        "//tf_keras/layers/locally_connected",
        "//tf_keras/layers/merging",
        "//tf_keras/layers/normalization",
        "//tf_keras/layers/pooling",
        "//tf_keras/layers/preprocessing",
        "//tf_keras/layers/regularization",
        "//tf_keras/layers/reshaping",
        "//tf_keras/layers/rnn",
        "//tf_keras/premade_models",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "kernelized",
    srcs = ["kernelized.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:base_layer",
        "//tf_keras/engine:input_spec",
        "//tf_keras/initializers",
        "@pypi//numpy",
    ],
)

py_library(
    name = "noise",
    srcs = ["noise.py"],
    deps = [
        "//tf_keras/layers/regularization:alpha_dropout",
        "//tf_keras/layers/regularization:gaussian_dropout",
        "//tf_keras/layers/regularization:gaussian_noise",
    ],
)

tf_py_test(
    name = "tensorflow_op_layer_test",
    size = "medium",
    srcs = ["tensorflow_op_layer_test.py"],
    shard_count = 3,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/saving",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

tf_py_test(
    name = "subclassed_layers_test",
    size = "medium",
    srcs = ["subclassed_layers_test.py"],
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
    name = "serialization_test",
    size = "small",
    srcs = ["serialization_test.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

tf_py_test(
    name = "kernelized_test",
    size = "small",
    srcs = ["kernelized_test.py"],
    deps = [
        ":layers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras/initializers",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "layers_test",
    size = "small",
    srcs = ["layers_test.py"],
    deps = [
        ":layers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)
