# Description:
#   Contains the TF-Keras engine API (internal TensorFlow version).

# Placeholder: load unaliased py_library

# buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")

# buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    # TODO(scottzhu): Remove non-keras deps from TF.
    default_visibility = ["//tf_keras:friends"],
    licenses = ["notice"],
)

py_library(
    name = "engine",
    srcs = [
        "__init__.py",
        "compile_utils.py",
        "functional.py",
        "partial_batch_padding_handler.py",
        "saving.py",
        "sequential.py",
        "training.py",
        "training_arrays_v1.py",
        "training_distributed_v1.py",
        "training_eager_v1.py",
        "training_generator_v1.py",
        "training_utils.py",
        "training_utils_v1.py",
        "training_v1.py",
    ],
    srcs_version = "PY3",
    deps = [
        ":base_layer",
        ":base_preprocessing_layer",
        ":data_adapter",
        ":functional_utils",
        ":input_layer",
        ":input_spec",
        ":keras_tensor",
        ":node",
        "//:expect_h5py_installed",
        "//:expect_tensorboard_installed",
        "//:expect_tensorflow_installed",
        "//:expect_yaml_installed",
        "//tf_keras:activations",
        "//tf_keras:backend",
        "//tf_keras:callbacks",
        "//tf_keras:callbacks_v1",
        "//tf_keras:constraints",
        "//tf_keras:losses",
        "//tf_keras:regularizers",
        "//tf_keras/distribute",
        "//tf_keras/distribute:distribute_coordinator_utils",
        "//tf_keras/dtensor:layout_map",
        "//tf_keras/export:export_lib",
        "//tf_keras/initializers",
        "//tf_keras/metrics",
        "//tf_keras/mixed_precision:autocast_variable",
        "//tf_keras/mixed_precision:loss_scale_optimizer",
        "//tf_keras/mixed_precision:policy",
        "//tf_keras/optimizers",
        "//tf_keras/saving",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:metrics_utils",
        "//tf_keras/utils:mode_keys",
        "//tf_keras/utils:steps_per_execution_tuning",
        "//tf_keras/utils:tf_utils",
        "//tf_keras/utils:version_utils",
    ],
)

py_library(
    name = "base_layer_utils",
    srcs = ["base_layer_utils.py"],
    srcs_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/dtensor",
        "//tf_keras/utils:tf_inspect",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "base_layer",
    srcs = [
        "base_layer.py",
        "base_layer_v1.py",
    ],
    srcs_version = "PY3",
    deps = [
        ":base_layer_utils",
        ":input_spec",
        ":node",
        "//:expect_numpy_installed",
        "//tf_keras:backend",
        "//tf_keras:constraints",
        "//tf_keras/initializers",
        # TODO(keras-team): Fix the circular deps between layer and metrics.
        # "//tf_keras/metrics",
        "//tf_keras:regularizers",
        "//tf_keras/dtensor:lazy_variable",
        "//tf_keras/mixed_precision:autocast_variable",
        "//tf_keras/mixed_precision:loss_scale_optimizer",
        "//tf_keras/mixed_precision:policy",
        "//tf_keras/saving",
        "//tf_keras/utils:generic_utils",
        "//tf_keras/utils:layer_utils",
        "//tf_keras/utils:object_identity",
        "//tf_keras/utils:tf_utils",
        "//tf_keras/utils:traceback_utils",
        "//tf_keras/utils:version_utils",
        "//:expect_tensorflow_installed",
    ],
)

py_library(
    name = "input_layer",
    srcs = ["input_layer.py"],
    deps = [
        ":base_layer",
        ":keras_tensor",
        ":node",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/distribute",
        "//tf_keras/saving",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "functional_utils",
    srcs = ["functional_utils.py"],
    deps = [
        ":input_layer",
        ":keras_tensor",
        ":node",
        "//:expect_tensorflow_installed",
    ],
)

py_library(
    name = "data_adapter",
    srcs = ["data_adapter.py"],
    srcs_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/distribute",
        "//tf_keras/utils:dataset_creator",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "input_spec",
    srcs = ["input_spec.py"],
    srcs_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
    ],
)

py_library(
    name = "keras_tensor",
    srcs = ["keras_tensor.py"],
    srcs_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/utils:object_identity",
        "//third_party/tensorflow/python/framework:none_tensor",
    ],
)

py_library(
    name = "base_preprocessing_layer",
    srcs = [
        "base_preprocessing_layer.py",
    ],
    srcs_version = "PY3",
    deps = [
        ":base_layer",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
    ],
)

py_library(
    name = "node",
    srcs = ["node.py"],
    srcs_version = "PY3",
    deps = [
        ":base_layer_utils",
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/utils:tf_utils",
    ],
)

tf_py_test(
    name = "base_layer_utils_test",
    srcs = ["base_layer_utils_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        ":base_layer_utils",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "data_adapter_test",
    size = "medium",
    srcs = ["data_adapter_test.py"],
    python_version = "PY3",
    shard_count = 4,
    tags = [
        "no_oss_py38",  # TODO(b/150615192)
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        ":data_adapter",
        "//:expect_numpy_installed",
        "//:expect_pandas_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "base_preprocessing_layer_test",
    size = "medium",
    srcs = ["base_preprocessing_layer_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        ":base_preprocessing_layer",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "functional_utils_test",
    size = "medium",
    srcs = ["functional_utils_test.py"],
    python_version = "PY3",
    deps = [
        ":functional_utils",
        ":input_layer",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "training_gpu_test",
    size = "small",
    srcs = ["training_gpu_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        ":engine",
        ":input_layer",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/layers/convolutional",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

tf_py_test(
    name = "correctness_test",
    size = "medium",
    srcs = ["correctness_test.py"],
    python_version = "PY3",
    shard_count = 2,
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
        "notsan",
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "keras_tensor_test",
    size = "small",
    srcs = ["keras_tensor_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "ragged_keras_tensor_test",
    size = "small",
    srcs = ["ragged_keras_tensor_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "input_spec_test",
    size = "small",
    srcs = ["input_spec_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
    ],
)

tf_py_test(
    name = "training_test",
    size = "large",  # TODO(keras-team): set back to medium after SWAP CL and investigate Timeouts
    srcs = ["training_test.py"],
    python_version = "PY3",
    shard_count = 20,
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
        "notsan",
    ],
    deps = [
        ":engine",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras:callbacks",
        "//tf_keras:losses",
        "//tf_keras/layers",
        "//tf_keras/metrics",
        "//tf_keras/mixed_precision:policy",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:data_utils",
        "//tf_keras/utils:np_utils",
    ],
)

tf_py_test(
    name = "compile_utils_test",
    size = "medium",
    srcs = ["compile_utils_test.py"],
    tags = [
        "nomac",  # TODO(b/146226927)
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "training_dataset_test",
    size = "medium",
    srcs = ["training_dataset_test.py"],
    python_version = "PY3",
    shard_count = 4,
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "training_arrays_test",
    size = "medium",
    srcs = ["training_arrays_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "training_generator_test",
    size = "medium",
    srcs = ["training_generator_test.py"],
    python_version = "PY3",
    shard_count = 6,
    tags = [
        "noasan",  # TODO(b/132183295): Re-enable this.
        "nomac",  # TODO(b/140193633): Re-enable this.
        "notsan",
    ],
    deps = [
        ":engine",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras:losses",
        "//tf_keras/layers",
        "//tf_keras/metrics",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:data_utils",
    ],
)

tf_py_test(
    name = "training_integration_test",
    size = "medium",
    srcs = ["training_integration_test.py"],
    python_version = "PY3",
    shard_count = 30,
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "feature_columns_integration_test",
    size = "medium",
    srcs = ["feature_columns_integration_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
        "notsan",
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "training_eager_test",
    size = "medium",
    srcs = ["training_eager_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
        "notsan",
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "training_utils_v1_test",
    size = "medium",
    srcs = ["training_utils_v1_test.py"],
    python_version = "PY3",
    tags = [
        "no_oss",  # TODO(b/135021748) re-enable
        "notsan",
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "input_layer_test",
    size = "medium",
    srcs = ["input_layer_test.py"],
    python_version = "PY3",
    shard_count = 3,
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        ":base_layer",
        ":engine",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:layer_utils",
    ],
)

tf_py_test(
    name = "functional_test",
    size = "medium",
    srcs = ["functional_test.py"],
    python_version = "PY3",
    shard_count = 8,
    tags = [
        "no-internal-py3",
        "no_rocm",
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        ":base_layer",
        ":engine",
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras/initializers",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:layer_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

tf_py_test(
    name = "node_test",
    size = "medium",
    srcs = ["node_test.py"],
    python_version = "PY3",
    shard_count = 3,
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        ":base_layer",
        ":engine",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:layer_utils",
    ],
)

tf_py_test(
    name = "base_layer_test",
    size = "medium",
    srcs = ["base_layer_test.py"],
    python_version = "PY3",
    shard_count = 8,
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        ":base_layer",
        ":engine",
        "//:expect_numpy_installed",
        "//:expect_tensorboard_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras:regularizers",
        "//tf_keras/layers",
        "//tf_keras/legacy_tf_layers:core",
        "//tf_keras/mixed_precision:policy",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

tf_py_test(
    name = "control_flow_test",
    size = "medium",
    srcs = ["control_flow_test.py"],
    python_version = "PY3",
    shard_count = 8,
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "sequential_test",
    size = "medium",
    srcs = ["sequential_test.py"],
    python_version = "PY3",
    shard_count = 4,
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "deferred_sequential_test",
    size = "medium",
    srcs = ["deferred_sequential_test.py"],
    python_version = "PY3",
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)
