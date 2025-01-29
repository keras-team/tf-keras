# Description:
#   Contains the TF-Keras Optimizer API.

# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "distribute_py_test")  # buildifier: disable=same-origin-load

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/python:__pkg__",
        "//third_party/tensorflow/python/distribute:__pkg__",
        "//third_party/tensorflow/python/saved_model:__pkg__",  # For unit tests.
        "//third_party/tensorflow/python/tpu/tests:__pkg__",  # For unit tests.
        "//third_party/tensorflow/python/trackable:__pkg__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "optimizers",
    srcs = [
        "__init__.py",
        "adadelta.py",
        "adafactor.py",
        "adagrad.py",
        "adam.py",
        "adamax.py",
        "adamw.py",
        "ftrl.py",
        "lion.py",
        "nadam.py",
        "optimizer.py",
        "optimizer_v1.py",
        "rmsprop.py",
        "sgd.py",
    ],
    deps = [
        ":utils",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/dtensor:utils",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/optimizers/schedules:learning_rate_schedule",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    deps = [
        "//:expect_tensorflow_installed",
    ],
)

py_library(
    name = "legacy_learning_rate_decay",
    srcs = ["legacy_learning_rate_decay.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/optimizers/schedules:learning_rate_schedule",
    ],
)

tf_py_test(
    name = "optimizer_v1_test",
    size = "medium",
    srcs = ["optimizer_v1_test.py"],
    shard_count = 8,
    tags = ["notsan"],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "legacy_learning_rate_decay_test",
    size = "medium",
    srcs = ["legacy_learning_rate_decay_test.py"],
    deps = [
        ":legacy_learning_rate_decay",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

# TODO(b/228209527): Combine this test with optimizer_test after
# fixing the NCCL issue.
distribute_py_test(
    name = "optimizer_pss_test",
    size = "medium",
    srcs = ["optimizer_pss_test.py"],
    shard_count = 50,
    tags = [
        "multi_gpu",
        "no_oss",
        "no_windows",
    ],
    deps = [
        ":optimizers",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

distribute_py_test(
    name = "optimizer_test",
    size = "medium",
    srcs = ["optimizer_test.py"],
    shard_count = 16,
    tags = [
        "multi_gpu",
        "no_windows",
        "nomultivm",  # TODO(b/203558991): Re-enable.
    ],
    deps = [
        ":optimizers",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "lion_test",
    size = "medium",
    srcs = ["lion_test.py"],
    shard_count = 4,
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
    ],
)
