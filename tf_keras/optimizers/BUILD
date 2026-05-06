# Description:
#   Contains the TF-Keras Optimizer API.

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "distribute_py_test")  # buildifier: disable=same-origin-load
load("@rules_python//python:py_library.bzl", "py_library")

package(
    default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/python:__pkg__",
        # "//third_party/tensorflow/python/distribute:__pkg__",
        # "//third_party/tensorflow/python/saved_model:__pkg__",  # For unit tests.
        # "//third_party/tensorflow/python/tpu/tests:__pkg__",  # For unit tests.
        # "//third_party/tensorflow/python/trackable:__pkg__",
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
    # copybara:uncomment strict_deps = False,
    deps = [
        ":utils",
        "# //third_party/py/absl/logging",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/dtensor:utils",
        "//tf_keras/initializers",
        "//tf_keras/mixed_precision:loss_scale_optimizer",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/optimizers/schedules:learning_rate_schedule",
        "//tf_keras/saving:object_registration",
        "//tf_keras/saving:serialization",
        "//tf_keras/saving:serialization_lib",
        "//tf_keras/utils:tf_utils",
        # "//third_party/tensorflow/python/util:core",
        "//third_party/tensorflow/tools/docs:doc_controls",
    ],
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    # copybara:uncomment strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        # "//third_party/tensorflow/python/platform:tf_logging",
    ],
)

py_library(
    name = "legacy_learning_rate_decay",
    srcs = ["legacy_learning_rate_decay.py"],
    # copybara:uncomment strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/optimizers/schedules:learning_rate_schedule",
        # "//third_party/tensorflow/python/util:core",
    ],
)

tf_py_test(
    name = "optimizer_v1_test",
    size = "medium",
    srcs = ["optimizer_v1_test.py"],
    shard_count = 8,
    tags = ["notsan"],
    deps = [
        ":optimizers",
        "@pypi//numpy",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:np_utils",
        # "//third_party/tensorflow/python/training:adam",
        # "//third_party/tensorflow/python/training/experimental:loss_scale_optimizer",
    ],
)

cuda_py_test(
    name = "legacy_learning_rate_decay_test",
    size = "medium",
    srcs = ["legacy_learning_rate_decay_test.py"],
    deps = [
        ":legacy_learning_rate_decay",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
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
        "# //third_party/py/absl/testing:parameterized",
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/utils:dataset_creator",
        "//tf_keras/utils:engine_utils",
    ],
)

distribute_py_test(
    name = "optimizer_test",
    size = "medium",
    srcs = ["optimizer_test.py"],
    shard_count = 16,
    # copybara:uncomment strict_deps = False,
    tags = [
        "multi_gpu",
        "no_windows",
        "nomultivm",  # TODO(b/203558991): Re-enable.
    ],
    deps = [
        "# //third_party/py/absl/testing:parameterized",
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/optimizers/schedules:learning_rate_schedule",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:engine_utils",
        "@pypi//portpicker",
    ],
)

cuda_py_test(
    name = "lion_test",
    size = "medium",
    srcs = ["lion_test.py"],
    shard_count = 4,
    deps = [
        ":optimizers",
        "@pypi//numpy",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        # "//third_party/tensorflow/python/framework:dtypes",
    ],
)
