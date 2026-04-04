# Description:
#   keras/distribute package is intended to serve as the centralized place for things
#   related to dist-strat used by TF-Keras..

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "distribute_py_test")  # buildifier: disable=same-origin-load
load("@rules_python//python:py_library.bzl", "py_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    # TODO(scottzhu): Remove this deps when distribute test are converted to integration test.
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/python/distribute:__pkg__",
        "//third_party/tensorflow/tools/pip_package:__pkg__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "distribute",
    srcs = [
        "__init__.py",
        "distributed_training_utils.py",
        "distributed_training_utils_v1.py",
    ],
    deps = [
        ":distribute_coordinator_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras:callbacks",
        "//tf_keras:callbacks_v1",
        "//tf_keras:constraints",
        "//tf_keras:losses",
        "//tf_keras:regularizers",
        "//tf_keras/initializers",
        "//tf_keras/mixed_precision:policy",
        "//tf_keras/optimizers",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:mode_keys",
    ],
)

py_library(
    name = "distribute_test_lib_pip",
    deps = [
        ":dataset_creator_model_fit_test_base",
        ":distribute_strategy_test_lib",
        ":keras_correctness_test_lib",
        ":keras_test_lib",
        ":model_combinations",
        ":multi_worker_testing_utils",
        ":saved_model_test_base",
        ":test_example",
    ],
)

py_library(
    name = "optimizer_combinations",
    srcs = ["optimizer_combinations.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/optimizers",
        "//tf_keras/optimizers/legacy:optimizers",
    ],
)

py_library(
    name = "worker_training_state",
    srcs = [
        "worker_training_state.py",
    ],
    deps = [
        ":distributed_file_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/utils:mode_keys",
    ],
)

py_library(
    name = "model_collection_base",
    srcs = ["model_collection_base.py"],
)

py_library(
    name = "model_combinations",
    srcs = ["model_combinations.py"],
    deps = [
        ":simple_models",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "simple_models",
    srcs = ["simple_models.py"],
    deps = [
        ":model_collection_base",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/optimizers/legacy:optimizers",
        "@pypi//numpy",
    ],
)

py_library(
    name = "saved_model_test_base",
    srcs = ["saved_model_test_base.py"],
    deps = [
        ":model_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

cuda_py_test(
    name = "model_checkpoint_test",
    srcs = ["model_checkpoint_test.py"],
    shard_count = 4,
    deps = [
        ":multi_worker_testing_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:callbacks",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

cuda_py_test(
    name = "worker_training_state_test",
    srcs = ["worker_training_state_test.py"],
    shard_count = 4,
    deps = [
        ":multi_worker_testing_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:callbacks",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

distribute_py_test(
    name = "checkpointing_test",
    srcs = ["checkpointing_test.py"],
    main = "checkpointing_test.py",
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/optimizers/legacy:optimizers",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

cuda_py_test(
    name = "collective_all_reduce_strategy_test",
    srcs = ["collective_all_reduce_strategy_test.py"],
    tags = [
        "multi_and_single_gpu",
        "nomsan",  # TODO(b/162894966)
        "notsan",  # TODO(b/171040408): data race
    ],
    # b/155301154 broken with XLA:GPU
    xla_enable_strict_auto_jit = True,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine",
        "//tf_keras/layers",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "ctl_correctness_test",
    srcs = ["ctl_correctness_test.py"],
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    main = "ctl_correctness_test.py",
    shard_count = 10,
    tags = [
        "multi_and_single_gpu",
        "no_cuda_asan",  # times out
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":optimizer_combinations",
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/applications",
        "//tf_keras/datasets",
        "//tf_keras/optimizers",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/tensorflow/python/ops/losses:losses_impl",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "custom_training_loop_metrics_test",
    srcs = ["custom_training_loop_metrics_test.py"],
    disable_mlir_bridge = False,
    main = "custom_training_loop_metrics_test.py",
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/metrics",
        "//third_party/tensorflow/python/framework:test_lib",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "custom_training_loop_models_test",
    srcs = ["custom_training_loop_models_test.py"],
    main = "custom_training_loop_models_test.py",
    tags = [
        "multi_and_single_gpu",
        "no_cuda_asan",  # times out
        "nomultivm",  # TODO(b/170502145)
        "notsan",  # TODO(b/170954243)
    ],
    tpu_tags = [
        "no_oss",  # b/153615544.
        "notsan",  # TODO(b/170869466)
    ],
    deps = [
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/layers/core",
        "//tf_keras/optimizers/legacy:optimizers",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "custom_training_loop_optimizer_test",
    srcs = ["custom_training_loop_optimizer_test.py"],
    disable_mlir_bridge = False,
    main = "custom_training_loop_optimizer_test.py",
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/optimizers/legacy:optimizers",
        "//third_party/tensorflow/python/distribute:values",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

py_library(
    name = "distribute_strategy_test_lib",
    srcs = [
        "distribute_strategy_test.py",
    ],
    deps = [
        ":distribute",
        ":multi_worker_testing_utils",
        ":optimizer_combinations",
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer_utils",
        "//tf_keras/mixed_precision:policy",
        "//tf_keras/optimizers",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:np_utils",
        "//third_party/tensorflow/python/distribute/cluster_resolver:cluster_resolver_lib",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

distribute_py_test(
    name = "keras_premade_models_test",
    size = "medium",
    srcs = ["keras_premade_models_test.py"],
    disable_mlir_bridge = False,
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    full_precision = True,
    main = "keras_premade_models_test.py",
    shard_count = 8,
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
        "requires-mem:28g",  # spawns multiple processes.
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine",
        "//tf_keras/layers/core",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/premade_models",
        "//tf_keras/utils:dataset_creator",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "distribute_strategy_test",
    size = "medium",
    srcs = ["distribute_strategy_test.py"],
    disable_mlir_bridge = True,  # TODO(b/170352626)
    full_precision = True,
    main = "distribute_strategy_test.py",
    shard_count = 20,
    tags = [
        "multi_and_single_gpu",
        "no_cuda_asan",  # TODO(b/182391774)
        "no_oss",  # TODO(b/191770103)
        "no_rocm",  # times out on ROCm
        "no_windows_gpu",
        "noguitar",  # TODO(b/172354344)
        "nomultivm",  # TODO(b/170502145)
        "notpu",  # b/188061768
        "notsan",
    ],
    tpu_tags = [
        "no_oss",  # b/155502591
    ],
    deps = [
        ":distribute",
        ":multi_worker_testing_utils",
        ":optimizer_combinations",
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer_utils",
        "//tf_keras/mixed_precision:policy",
        "//tf_keras/optimizers",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:np_utils",
        "//third_party/tensorflow/python/distribute/cluster_resolver:cluster_resolver_lib",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "distributed_training_utils_test",
    srcs = ["distributed_training_utils_test.py"],
    disable_mlir_bridge = False,
    full_precision = True,
    main = "distributed_training_utils_test.py",
    tags = [
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":distribute",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:callbacks",
        "//tf_keras/metrics",
        "//tf_keras/optimizers/legacy:optimizers",
    ],
)

py_library(
    name = "keras_correctness_test_lib",
    srcs = [
        "keras_correctness_test_base.py",
        "keras_dnn_correctness_test.py",
        "keras_embedding_model_correctness_test.py",
        "keras_image_model_correctness_test.py",
        "keras_rnn_model_correctness_test.py",
        "keras_stateful_lstm_model_correctness_test.py",
    ],
    deps = [
        ":distribute",
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras/layers/rnn:gru",
        "//tf_keras/layers/rnn:gru_v1",
        "//tf_keras/layers/rnn:lstm",
        "//tf_keras/layers/rnn:lstm_v1",
        "//tf_keras/mixed_precision:policy",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:data_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

distribute_py_test(
    name = "keras_dnn_correctness_test",
    size = "medium",
    srcs = ["keras_dnn_correctness_test.py"],
    disable_mlir_bridge = True,  # TODO(b/170352626)
    full_precision = True,
    main = "keras_dnn_correctness_test.py",
    # Shard count is set to an odd number to distribute tasks across
    # shards more evenly.
    shard_count = 19,
    tags = [
        "multi_and_single_gpu",
        "no_oss",  # TODO(b/173021094)
        "no_rocm",  # times out on ROCm
        "no_windows_gpu",
        "nogpu",  # TODO(b/170905292)
        "nomultivm",  # TODO(b/170502145)
        "notap",  # TODO(b/178803051): flaky
        "notsan",
    ],
    deps = [
        ":keras_correctness_test_lib",
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "keras_embedding_model_correctness_test",
    size = "medium",
    srcs = ["keras_embedding_model_correctness_test.py"],
    disable_mlir_bridge = True,  # TODO(b/170352626)
    full_precision = True,
    main = "keras_embedding_model_correctness_test.py",
    shard_count = 8,
    tags = [
        "broken",  # b/170975619
        "multi_and_single_gpu",
        "no_cuda_asan",  # times out
        "no_rocm",
        "no_windows_gpu",
        "nomultivm",  # TODO(b/170502145)
        "notsan",
    ],
    deps = [
        ":keras_correctness_test_lib",
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "keras_image_model_correctness_test",
    size = "medium",
    srcs = ["keras_image_model_correctness_test.py"],
    disable_mlir_bridge = True,  # TODO(b/170352626)
    full_precision = True,
    main = "keras_image_model_correctness_test.py",
    shard_count = 16,
    tags = [
        "multi_and_single_gpu",
        "no_rocm",  # times out on ROCm
        "no_windows_gpu",
        "noasan",  # TODO(b/337374867) fails with -fsanitize=null
        "nomultivm",  # TODO(b/170502145)
        "notpu",  # TODO(b/210148661)
        "notsan",
    ],
    xla_enable_strict_auto_jit = False,  # Tensorflow also fails.
    deps = [
        ":keras_correctness_test_lib",
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "keras_metrics_test",
    srcs = ["keras_metrics_test.py"],
    disable_mlir_bridge = False,
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    main = "keras_metrics_test.py",
    shard_count = 8,
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine:base_layer",
        "//tf_keras/metrics",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "keras_models_test",
    srcs = ["keras_models_test.py"],
    main = "keras_models_test.py",
    tags = [
        "multi_and_single_gpu",
        "no_oss",  # TODO(b/202850066)
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

distribute_py_test(
    name = "keras_rnn_model_correctness_test",
    size = "medium",
    srcs = ["keras_rnn_model_correctness_test.py"],
    full_precision = True,
    main = "keras_rnn_model_correctness_test.py",
    # Shard count is set to an odd number to distribute tasks across
    # shards more evenly.
    shard_count = 31,
    tags = [
        "multi_and_single_gpu",
        "no_oss",  # TODO(b/277925387)
        "no_rocm",  # Would require size large, but that effectively disables the test for presubmits.
        "no_windows_gpu",
        "noasan",  # TODO(b/337374867) fails with -fsanitize=null
        "nomultivm",  # TODO(b/170502145)
        "notpu",  # TODO(b/153672562)
        "notsan",
    ],
    deps = [
        ":keras_correctness_test_lib",
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "keras_save_load_test",
    size = "medium",
    srcs = ["keras_save_load_test.py"],
    full_precision = True,
    main = "keras_save_load_test.py",
    shard_count = 7,
    tags = [
        "multi_and_single_gpu",
        "no_rocm",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":saved_model_test_base",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/saving",
        "//tf_keras/testing_infra:test_utils",
    ],
)

distribute_py_test(
    name = "keras_stateful_lstm_model_correctness_test",
    size = "medium",
    srcs = ["keras_stateful_lstm_model_correctness_test.py"],
    disable_mlir_bridge = False,
    full_precision = True,
    main = "keras_stateful_lstm_model_correctness_test.py",
    shard_count = 4,
    tags = [
        "multi_and_single_gpu",
        "no_pip",
        "no_windows_gpu",
        "nomultivm",  # TODO(b/170502145)
        "notsan",
    ],
    deps = [
        ":keras_correctness_test_lib",
    ],
)

distribute_py_test(
    name = "keras_utils_test",
    srcs = ["keras_utils_test.py"],
    disable_mlir_bridge = True,  # TODO(b/170352626)
    full_precision = True,
    main = "keras_utils_test.py",
    shard_count = 4,
    tags = [
        "multi_and_single_gpu",
        "no_cuda_asan",  # times out
        "no_pip",  # The test imports distribute_strategy_test which is not in the pip package.
        "no_windows_gpu",
        "nomultivm",  # TODO(b/170502145)
        "notsan",
    ],
    deps = [
        ":distribute",
        ":distribute_strategy_test_lib",
        ":optimizer_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:losses",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

py_library(
    name = "keras_test_lib",
    srcs = [
        "keras_utils_test.py",
    ],
    deps = [
        ":distribute",
        ":distribute_strategy_test_lib",
        ":optimizer_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:losses",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

cuda_py_test(
    name = "keras_optimizer_v2_test",
    srcs = ["keras_optimizer_v2_test.py"],
    shard_count = 4,
    tags = [
        "multi_and_single_gpu",
        "tf_integration_test",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/optimizers/legacy:optimizers",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

distribute_py_test(
    name = "minimize_loss_test",
    srcs = ["minimize_loss_test.py"],
    main = "minimize_loss_test.py",
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":optimizer_combinations",
        ":test_example",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/layers/core",
        "//tf_keras/optimizers/legacy:optimizers",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

cuda_py_test(
    name = "mirrored_strategy_test",
    srcs = ["mirrored_strategy_test.py"],
    tags = [
        "multi_and_single_gpu",
        "no_windows_gpu",  # TODO(b/130551176)
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/engine",
        "//tf_keras/layers/core",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/utils:kpl_test_utils",
        "//third_party/tensorflow/python/eager:backprop",
        "//third_party/tensorflow/python/training:optimizer",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

cuda_py_test(
    name = "mirrored_variable_test",
    srcs = ["mirrored_variable_test.py"],
    tags = [
        "guitar",
        "multi_and_single_gpu",
    ],
    deps = [
        ":distribute",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/layers/core",
        "//tf_keras/metrics",
    ],
)

cuda_py_test(
    name = "multi_worker_test",
    srcs = ["multi_worker_test.py"],
    shard_count = 2,
    tags = [
        "multi_and_single_gpu",
        "no_oss",  # TODO(b/130369494): Investigate why it times out on OSS.
    ],
    deps = [
        ":multi_worker_testing_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras:callbacks",
        "//tf_keras/metrics",
        "//tf_keras/models",
        "//tf_keras/optimizers",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/utils:kpl_test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

tf_py_test(
    name = "multi_worker_callback_tf2_test",
    srcs = ["multi_worker_callback_tf2_test.py"],
    shard_count = 5,
    tags = [
        "no_windows",  # TODO(b/184424727): Re-enable this.
    ],
    deps = [
        ":distributed_file_utils",
        ":multi_worker_testing_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:callbacks",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//portpicker",
    ],
)

py_library(
    name = "multi_worker_testing_utils",
    srcs = [
        "multi_worker_testing_utils.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/optimizers/legacy:optimizers",
        "//third_party/py/portpicker",
        "//third_party/tensorflow/python/distribute/cluster_resolver:cluster_resolver_lib",
        "//third_party/tensorflow/python/training:server_lib",
    ],
)

py_library(
    name = "tpu_strategy_test_utils",
    srcs = ["tpu_strategy_test_utils.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//third_party/py/absl/flags",
    ],
)

distribute_py_test(
    name = "saved_model_save_load_test",
    size = "medium",
    srcs = ["saved_model_save_load_test.py"],
    full_precision = True,
    main = "saved_model_save_load_test.py",
    shard_count = 7,
    tags = [
        "multi_and_single_gpu",
        "no_cuda_asan",  # times out
        "no_rocm",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":model_combinations",
        ":saved_model_test_base",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_utils",
    ],
)

distribute_py_test(
    name = "saved_model_mixed_api_test",
    size = "medium",
    srcs = ["saved_model_mixed_api_test.py"],
    full_precision = True,
    main = "saved_model_mixed_api_test.py",
    shard_count = 7,
    tags = [
        "multi_and_single_gpu",
        "no_rocm",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":saved_model_test_base",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/saving",
        "//tf_keras/testing_infra:test_utils",
    ],
)

distribute_py_test(
    name = "sharded_variable_test",
    srcs = ["sharded_variable_test.py"],
    shard_count = 2,
    tags = [
        "multi_and_single_gpu",
        "no_rocm",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":multi_worker_testing_utils",
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/engine:base_layer",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "parameter_server_evaluation_test",
    srcs = ["parameter_server_evaluation_test.py"],
    shard_count = 1,
    tags = [
        "multi_and_single_gpu",
        "no_cuda_asan",  # TODO(b/186361027)
        "no_oss",  # TODO(b/186248973)
        "no_tfrt",
        "nomultivm",  # TODO(b/170502145)
        "notpu",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/tensorflow/python/distribute:multi_worker_test_base",
        "//third_party/tensorflow/python/distribute/cluster_resolver:cluster_resolver_lib",
        "//third_party/tensorflow/python/ops:variables",
    ],
)

distribute_py_test(
    name = "parameter_server_exact_evaluation_test",
    srcs = ["parameter_server_exact_evaluation_test.py"],
    shard_count = 29,
    tags = [
        "multi_and_single_gpu",
        "no_cuda_asan",  # TODO(b/186361027)
        "no_oss",  # TODO(b/186248973)
        "no_tfrt",
        "nomultivm",  # TODO(b/170502145)
        "notpu",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/metrics",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:dataset_creator",
        "//tf_keras/utils:tf_utils",
        "//third_party/tensorflow/python/distribute:multi_worker_test_base",
        "//third_party/tensorflow/python/distribute/cluster_resolver:cluster_resolver_lib",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

distribute_py_test(
    name = "dataset_creator_model_fit_test",
    srcs = ["dataset_creator_model_fit_test.py"],
    disable_mlir_bridge = True,  # TODO(b/170352626)
    disable_tpu_use_tfrt = True,  # TODO(b/195081590)
    full_precision = True,
    main = "dataset_creator_model_fit_test.py",
    shard_count = 50,
    tags = [
        "multi_gpu",
        "no_oss",  # TODO(b/183640564): Re-enable
        "no_rocm",
        "nomultivm",  # TODO(b/170502145)
        "notpu",  # TODO(b/210168103)
        "notsan",  # TODO(b/184542721)
    ],
    deps = [
        ":dataset_creator_model_fit_test_base",
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:dataset_creator",
        "//third_party/tensorflow/python/framework:test_lib",
        "@pypi//portpicker",
    ],
)

distribute_py_test(
    name = "dataset_creator_model_fit_ps_only_test",
    size = "medium",
    srcs = ["dataset_creator_model_fit_ps_only_test.py"],
    disable_mlir_bridge = True,  # TODO(b/170352626)
    full_precision = True,
    main = "dataset_creator_model_fit_ps_only_test.py",
    shard_count = 21,
    tags = [
        "multi_gpu",
        "no_oss",  # TODO(b/183640564): Re-enable
        "no_rocm",
        "nomultivm",  # TODO(b/170502145)
        "notsan",  # TODO(b/184542721)
    ],
    deps = [
        ":dataset_creator_model_fit_test_base",
        ":strategy_combinations",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:callbacks",
        "//tf_keras/testing_infra:test_utils",
    ],
)

py_library(
    name = "distributed_file_utils",
    srcs = [
        "distributed_file_utils.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//third_party/py/requests",
    ],
)

tf_py_test(
    name = "distributed_file_utils_test",
    srcs = ["distributed_file_utils_test.py"],
    deps = [
        ":distributed_file_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "strategy_combinations",
    srcs = ["strategy_combinations.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "test_example",
    srcs = ["test_example.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/legacy_tf_layers:core",
        "//tf_keras/legacy_tf_layers:normalization",
        "//tf_keras/optimizers/legacy:optimizers",
    ],
)

py_library(
    name = "distribute_coordinator_utils",
    srcs = [
        "distribute_coordinator_utils.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//third_party/tensorflow/core/protobuf:for_core_protos_py_proto",
    ],
)

py_library(
    name = "dataset_creator_model_fit_test_base",
    srcs = [
        "dataset_creator_model_fit_test_base.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:callbacks",
        "//tf_keras/engine",
        "//tf_keras/layers/core",
        "//tf_keras/layers/preprocessing:string_lookup",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/utils:dataset_creator",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)
