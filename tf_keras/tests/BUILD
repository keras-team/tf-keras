# Description:
#   Contains TF-Keras test utils and integration tests.

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tpu_py_test")  # buildifier: disable=same-origin-load
load("@rules_python//python:py_library.bzl", "py_library")
load("@rules_python//python:py_test.bzl", "py_test")

package(
    default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/tools/pip_package:__pkg__",
    ],
    licenses = ["notice"],
)

tf_py_test(
    name = "get_config_test",
    srcs = ["get_config_test.py"],
    shard_count = 4,
    tags = [
        "no_pip",
    ],
    deps = [
        ":get_config_samples",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/engine",
        "//tf_keras/testing_infra:test_combinations",
        "//third_party/py/tensorflow:tensorflow_core",
    ],
)

tf_py_test(
    name = "add_loss_correctness_test",
    srcs = ["add_loss_correctness_test.py"],
    shard_count = 4,
    deps = [
        "//tf_keras",
        "//tf_keras:losses",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/layers",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/platform:tf_logging",
        # "//third_party/tensorflow/python/training:rmsprop",
    ],
)

tpu_py_test(
    name = "automatic_outside_compilation_test",
    srcs = [
        "automatic_outside_compilation_test.py",
    ],
    disable_experimental = True,
    disable_mlir_bridge = False,
    tags = ["no_oss"],
    deps = [
        "//tf_keras:callbacks",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/distribute:distribute_strategy_test_lib",
        "//tf_keras/engine",
        "//tf_keras/engine:base_layer",
        "//tf_keras/layers/convolutional",
        "//tf_keras/layers/core",
        "//tf_keras/layers/pooling",
        "//tf_keras/layers/regularization",
        "//tf_keras/layers/reshaping",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/py/absl/flags",
        "@pypi//numpy",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/eager:context",
        # "//third_party/tensorflow/python/framework:test_lib",
    ],
)

tf_py_test(
    name = "convert_to_constants_test",
    srcs = ["convert_to_constants_test.py"],
    shard_count = 4,
    deps = [
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/framework:convert_to_constants",
        # "//third_party/tensorflow/python/saved_model:load",
        # "//third_party/tensorflow/python/saved_model:save",
    ],
)

tf_py_test(
    name = "custom_training_loop_test",
    srcs = ["custom_training_loop_test.py"],
    shard_count = 4,
    tags = ["notsan"],
    deps = [
        "# //third_party/py/absl/testing:parameterized",
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/py/tensorflow:tensorflow_core",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "graph_util_test",
    srcs = ["graph_util_test.py"],
    deps = [
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/core/protobuf:for_core_protos_py_proto",
        # "//third_party/tensorflow/python/grappler:tf_optimizer",
        # "//third_party/tensorflow/python/training:saver",
    ],
)

tf_py_test(
    name = "integration_test",
    size = "medium",
    srcs = ["integration_test.py"],
    shard_count = 16,
    tags = [
        "notsan",
    ],
    deps = [
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/layers/rnn:legacy_cells",
        "//tf_keras/legacy_tf_layers:layers_base",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils",
        "//third_party/py/tensorflow:tensorflow_core",
        "@pypi//numpy",
    ],
)

py_library(
    name = "model_architectures",
    srcs = [
        "model_architectures.py",
    ],
    # copybara:uncomment strict_deps = False,
    deps = [
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
    ],
)

tf_py_test(
    name = "model_architectures_test",
    srcs = ["model_architectures_test.py"],
    shard_count = 16,
    deps = [
        "# //third_party/py/absl/testing:parameterized",
        ":model_architectures",
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/py/tensorflow:tensorflow_core",
        "@pypi//numpy",
    ],
)

py_library(
    name = "model_subclassing_test_util",
    srcs = ["model_subclassing_test_util.py"],
    # copybara:uncomment strict_deps = False,
    deps = [
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/testing_infra:test_utils",
    ],
)

tf_py_test(
    name = "model_subclassing_test",
    srcs = ["model_subclassing_test.py"],
    shard_count = 4,
    tags = [
        "no_windows",
        "notsan",
    ],
    deps = [
        ":model_subclassing_test_util",
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "# //third_party/py/absl/testing:parameterized",
        "@pypi//numpy",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/framework:test_lib",
        # "//third_party/tensorflow/python/trackable:data_structures",
    ],
)

tf_py_test(
    name = "model_subclassing_compiled_test",
    srcs = ["model_subclassing_compiled_test.py"],
    shard_count = 4,
    tags = [
        "no_windows",
        "notsan",
    ],
    deps = [
        ":model_subclassing_test_util",
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/py/tensorflow:tensorflow_core",
        "@pypi//numpy",
    ],
)

cuda_py_test(
    name = "memory_test",
    size = "medium",
    srcs = ["memory_test.py"],
    tags = [
        "no_oss",
        "optonly",  # The test is too slow in non-opt mode
    ],
    # TODO(b/140065350): Re-enable
    xla_enable_strict_auto_jit = False,
    deps = [
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/eager/memory_tests:memory_test_util",
    ],
)

tf_py_test(
    name = "memory_checker_test",
    size = "medium",
    srcs = ["memory_checker_test.py"],
    shard_count = 8,
    tags = [
        "no_oss",
        "no_pip",
        "no_windows",
        "noasan",  # TODO(b/149948895): Re-enable.
        "nomsan",  # TODO(b/149948895): Re-enable.
        "notsan",  # TODO(b/149948895): Re-enable.
    ],
    deps = [
        "//tf_keras/api:tf_keras_api",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        # "//third_party/tensorflow/python/framework:memory_checker",
    ],
)

tf_py_test(
    name = "saved_model_test",
    size = "small",
    srcs = ["saved_model_test.py"],
    tags = [
        "no_oss",  # TODO(b/170766453)
        "notap",  # TODO(b/170766453)
    ],
    deps = [
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/layers/core",
        "//tf_keras/optimizers/legacy:optimizers",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/framework:test_lib",
    ],
)

cuda_py_test(
    name = "saver_test",
    size = "medium",
    srcs = ["saver_test.py"],
    deps = [
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/engine",
        "//tf_keras/layers/core",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/checkpoint",
    ],
)

tf_py_test(
    name = "serialization_util_test",
    size = "small",
    srcs = ["serialization_util_test.py"],
    deps = [
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/engine",
        "//tf_keras/engine:input_layer",
        "//tf_keras/layers/core",
        "//tf_keras/saving/legacy/saved_model",
        "//tf_keras/testing_infra:test_combinations",
        "//third_party/py/tensorflow:tensorflow_core",
    ],
)

tf_py_test(
    name = "temporal_sample_weights_correctness_test",
    srcs = ["temporal_sample_weights_correctness_test.py"],
    shard_count = 20,
    deps = [
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/layers",
        "//tf_keras/metrics",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/py/tensorflow:tensorflow_core",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "tracking_test",
    srcs = ["tracking_test.py"],
    tags = [
        "no_windows",
        "nomac",
    ],
    deps = [
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/engine",
        "//tf_keras/layers/core",
        "//tf_keras/layers/normalization:batch_normalization_v1",
        "//tf_keras/testing_infra:test_combinations",
        "# //third_party/py/absl/testing:parameterized",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/checkpoint",
        # "//third_party/tensorflow/python/trackable:data_structures",
    ],
)

tf_py_test(
    name = "tracking_util_test",
    srcs = ["tracking_util_test.py"],
    tags = ["notsan"],  # b/74395663
    deps = [
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/engine",
        "//tf_keras/engine:input_layer",
        "//tf_keras/layers/core",
        "//tf_keras/layers/reshaping",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/checkpoint",
        # "//third_party/tensorflow/python/eager:context",
        # "//third_party/tensorflow/python/framework:test_lib",
        # "//third_party/tensorflow/python/platform:tf_logging",
    ],
)

tf_py_test(
    name = "tracking_util_with_v1_optimizers_test",
    srcs = ["tracking_util_with_v1_optimizers_test.py"],
    tags = [
        "no_windows",  # TODO(b/184424727): Re-enable this.
        "notsan",  # b/74395663
    ],
    deps = [
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/engine",
        "//tf_keras/layers/core",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/py/tensorflow:tensorflow_core",
        # "//third_party/tensorflow/python/checkpoint",
        # "//third_party/tensorflow/python/eager:context",
        # "//third_party/tensorflow/python/framework:test_lib",
    ],
)

py_library(
    name = "get_config_samples",
    srcs = [
        "__init__.py",
        "get_config_samples.py",
    ],
    # copybara:uncomment strict_deps = False,
    deps = ["//tf_keras/api:tf_keras_api"],
)

py_test(
    name = "keras_doctest",
    srcs = ["keras_doctest.py"],
    # copybara:uncomment strict_deps = False,
    tags = [
        "no_pip",
        "noasan",
        "nomsan",
        "notsan",
    ],
    deps = [
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/testing_infra:keras_doctest_lib",
        "//third_party/py/absl/flags",
        "//third_party/py/absl/testing:absltest",
        "//third_party/py/tensorflow:tensorflow_core",
        "@pypi//numpy",
    ],
)
