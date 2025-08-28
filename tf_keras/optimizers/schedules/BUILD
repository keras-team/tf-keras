# Description:
#   Contains the learning rate schedule API,

# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = ["//tf_keras:friends"],
    licenses = ["notice"],
)

py_library(
    name = "learning_rate_schedule",
    srcs = [
        "__init__.py",
        "learning_rate_schedule.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/utils:generic_utils",
    ],
)

cuda_py_test(
    name = "learning_rate_schedule_test",
    size = "medium",
    srcs = ["learning_rate_schedule_test.py"],
    shard_count = 4,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)
