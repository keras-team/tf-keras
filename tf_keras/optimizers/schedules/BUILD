# Description:
#   Contains the learning rate schedule API,

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")
load("@rules_python//python:py_library.bzl", "py_library")

package(
    default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = ["//tf_keras:friends"],
    licenses = ["notice"],
)

py_library(
    name = "learning_rate_schedule",
    srcs = [
        "__init__.py",
        "learning_rate_schedule.py",
    ],
    # copybara:uncomment strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/saving:serialization",
        "//tf_keras/saving:serialization_lib",
        # "//third_party/tensorflow/python/util:core",
    ],
)

cuda_py_test(
    name = "learning_rate_schedule_test",
    size = "medium",
    srcs = ["learning_rate_schedule_test.py"],
    shard_count = 4,
    deps = [
        "# //third_party/py/absl/testing:parameterized",
        ":learning_rate_schedule",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)
