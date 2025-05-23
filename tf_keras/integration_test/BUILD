# Description:
#   Contains TF-Keras integration tests that verify with other TF high level APIs.

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "distribute_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tpu_py_test")  # buildifier: disable=same-origin-load
# Placeholder: load unaliased py_library

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/tools/pip_package:__pkg__",
    ],
    licenses = ["notice"],
)

tf_py_test(
    name = "forwardprop_test",
    srcs = ["forwardprop_test.py"],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

tf_py_test(
    name = "function_test",
    srcs = ["function_test.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

tf_py_test(
    name = "gradients_test",
    srcs = ["gradients_test.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

cuda_py_test(
    name = "saved_model_test",
    srcs = ["saved_model_test.py"],
    tags = [
        "no_oss",  # TODO(keras-team): Fails in OSS due to reference to `tf.keras`
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

tf_py_test(
    name = "legacy_rnn_test",  # Remove this target in when TF 1 is deprecated.
    srcs = ["legacy_rnn_test.py"],
    tags = [
        "no_oss",  # TODO(keras-team): Fails in OSS cpu tests due to lazy loading of `keras` module.
    ],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

tf_py_test(
    name = "module_test",
    srcs = ["module_test.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

tf_py_test(
    name = "vectorized_map_test",
    srcs = ["vectorized_map_test.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

cuda_py_test(
    name = "gradient_checkpoint_test",
    srcs = ["gradient_checkpoint_test.py"],
    tags = ["no_oss"],  # TODO(b/249526796)
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

cuda_py_test(
    name = "central_storage_strategy_test",
    srcs = ["central_storage_strategy_test.py"],
    tags = [
        "multi_and_single_gpu",
        "no_oss",  # TODO(keras-team): Fails in OSS due to reference to `tf.keras`.
        "no_windows_gpu",  # TODO(b/130551176)
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/utils:kpl_test_utils",
    ],
)

tpu_py_test(
    name = "tpu_strategy_test",
    srcs = ["tpu_strategy_test.py"],
    disable_experimental = True,
    disable_mlir_bridge = False,
    tags = ["no_oss"],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
    ],
)

tf_py_test(
    name = "multi_worker_tutorial_test",
    srcs = ["multi_worker_tutorial_test.py"],
    shard_count = 6,
    tags = [
        "no_oss",  # TODO(keras-team): Fails in OSS cpu tests due to reference to `tf.keras`.
        "no_windows",  # TODO(b/183102726)
        "noasan",  # TODO(b/156029134)
        "nomac",  # TODO(b/182567880)
        "nomsan",  # TODO(b/156029134)
        "notsan",  # TODO(b/156029134)
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_portpicker_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

distribute_py_test(
    name = "ctl_tutorial_test",
    srcs = ["ctl_tutorial_test.py"],
    main = "ctl_tutorial_test.py",
    shard_count = 5,
    tags = [
        "multi_and_single_gpu",
        "no_oss",  # TODO(keras-team): Fails in OSS due to references to `tf.keras`
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/distribute:strategy_combinations",
    ],
)

distribute_py_test(
    name = "parameter_server_keras_preprocessing_test",
    srcs = ["parameter_server_keras_preprocessing_test.py"],
    shard_count = 6,  # TODO(b/184290570): Investigate why only 1 shard times out.
    tags = [
        "multi_and_single_gpu",
        "no_oss",  # TODO(b/194935930): Flaky test
        "nomultivm",  # TODO(b/170502145)
        "notap",  # b/216629693
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_portpicker_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/testing_infra:test_utils",
    ],
)

distribute_py_test(
    name = "distributed_training_test",
    srcs = ["distributed_training_test.py"],
    shard_count = 50,
    tags = [
        "multi_gpu",
        "no_oss",  # TODO(b/183640564): Re-enable
        "no_rocm",
        "noasan",  # TODO(b/184542721)
        "nomsan",  # TODO(b/184542721)
        "nomultivm",  # TODO(b/170502145)
        "notsan",  # TODO(b/184542721)
    ],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

distribute_py_test(
    name = "mwms_multi_process_runner_test",
    srcs = ["mwms_multi_process_runner_test.py"],
    tags = [
        "multi_gpu",
        "no_rocm",
        "noasan",  # TODO(b/184542721)
        "nomsan",  # TODO(b/184542721)
        "nomultivm",  # TODO(b/170502145)
        "notpu",
        "notsan",  # TODO(b/184542721)
    ],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

py_library(
    name = "preprocessing_test_utils",
    srcs = ["preprocessing_test_utils.py"],
    deps = ["//:expect_tensorflow_installed"],
)

distribute_py_test(
    name = "preprocessing_applied_in_dataset_creator_test",
    srcs = ["preprocessing_applied_in_dataset_creator_test.py"],
    shard_count = 50,
    tags = [
        "multi_gpu",
        "no_oss",  # TODO(b/183640564): Re-enable
        "no_rocm",
        "noasan",  # TODO(b/184542721)
        "nomsan",  # TODO(b/184542721)
        "nomultivm",  # TODO(b/170502145)
        "notsan",  # TODO(b/184542721)
    ],
    deps = [
        ":preprocessing_test_utils",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

distribute_py_test(
    name = "preprocessing_applied_in_dataset_test",
    srcs = ["preprocessing_applied_in_dataset_test.py"],
    shard_count = 50,
    tags = [
        "multi_gpu",
        "no_oss",  # TODO(b/183640564): Re-enable
        "no_rocm",
        "noasan",  # TODO(b/184542721)
        "nomsan",  # TODO(b/184542721)
        "nomultivm",  # TODO(b/170502145)
        "notsan",  # TODO(b/184542721)
    ],
    deps = [
        ":preprocessing_test_utils",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

distribute_py_test(
    name = "preprocessing_applied_in_model_test",
    srcs = ["preprocessing_applied_in_model_test.py"],
    shard_count = 50,
    tags = [
        "multi_gpu",
        "no_oss",  # TODO(b/183640564): Re-enable
        "no_rocm",
        "noasan",  # TODO(b/184542721)
        "nomsan",  # TODO(b/184542721)
        "nomultivm",  # TODO(b/170502145)
        "notsan",  # TODO(b/184542721)
    ],
    deps = [
        ":preprocessing_test_utils",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

distribute_py_test(
    name = "parameter_server_custom_training_loop_test",
    srcs = ["parameter_server_custom_training_loop_test.py"],
    tags = [
        "multi_gpu",
        "no_oss",  # TODO(b/183640564): Re-enable
        "no_rocm",
        "noasan",  # TODO(b/184542721)
        "nomsan",  # TODO(b/184542721)
        "nomultivm",  # TODO(b/170502145)
        "notsan",  # TODO(b/184542721)
    ],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
    ],
)

tf_py_test(
    name = "custom_object_saving_test",
    srcs = ["custom_object_saving_test.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "parameter_server_training_metric_test",
    srcs = ["parameter_server_training_metric_test.py"],
    tags = [
        "nomac",  # TODO(mihaimaruseac): b/127695564
        "notsan",  # TODO(b/156029134)
    ],
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "fit_test",
    size = "medium",
    srcs = ["fit_test.py"],
    shard_count = 28,
    tags = [
        "no_oss",  # TODO(keras-team): Fails in OSS due to reference to `tf.keras`
    ],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/integration_test/models",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "saving_v3_test",
    size = "medium",
    srcs = ["saving_v3_test.py"],
    shard_count = 12,
    tags = [
        "no_oss",  # TODO(keras-team): Fails in OSS.
    ],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/integration_test/models",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "py_metric_test",
    size = "medium",
    srcs = ["py_metric_test.py"],
    shard_count = 2,
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/metrics",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "extension_type_test",
    size = "medium",
    srcs = ["extension_type_test.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/engine",
        "//tf_keras/engine:input_layer",
        "//tf_keras/saving",
    ],
)
