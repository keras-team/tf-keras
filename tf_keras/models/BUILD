# TF-Keras models

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "distribute_py_test")  # buildifier: disable=same-origin-load
load("@rules_python//python:py_library.bzl", "py_library")

package(
    default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
    ],
    licenses = ["notice"],
)

py_library(
    name = "sharpness_aware_minimization",
    srcs = ["sharpness_aware_minimization.py"],
    # copybara:uncomment strict_deps = False,
    deps = [
        ":cloning",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine:data_adapter",
        "//tf_keras/layers",
        "//tf_keras/saving:object_registration",
        "//tf_keras/saving:serialization_lib",
        # "//third_party/tensorflow/python/util:core",
    ],
)

py_library(
    name = "models",
    srcs = [
        "__init__.py",
    ],
    # copybara:uncomment strict_deps = False,
    deps = [
        ":cloning",
        ":sharpness_aware_minimization",
        "//tf_keras/engine",
        "//tf_keras/saving",
    ],
)

py_library(
    name = "cloning",
    srcs = [
        "cloning.py",
    ],
    # copybara:uncomment strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:input_layer",
        "//tf_keras/metrics",
        "//tf_keras/optimizers",
        "//tf_keras/saving:object_registration",
        "//tf_keras/saving:serialization",
        "//tf_keras/saving/legacy/saved_model:utils",
        "//tf_keras/utils:generic_utils",
        "//tf_keras/utils:version_utils",
        # "//third_party/tensorflow/python/platform:tf_logging",
        # "//third_party/tensorflow/python/util:core",
    ],
)

tf_py_test(
    name = "cloning_test",
    size = "medium",
    srcs = ["cloning_test.py"],
    main = "cloning_test.py",
    shard_count = 8,
    tags = [
        "notsan",  # b/67509773
    ],
    deps = [
        "# //third_party/py/absl/testing:parameterized",
        ":models",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras/metrics",
        "//tf_keras/optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

distribute_py_test(
    name = "sharpness_aware_minimization_test",
    size = "medium",
    srcs = ["sharpness_aware_minimization_test.py"],
    shard_count = 8,
    tags = [
        "multi_gpu",
        "nomultivm",
        "requires-net:ipv4",
    ],
    deps = [
        "# //third_party/py/absl/testing:parameterized",
        ":sharpness_aware_minimization",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/optimizers",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//portpicker",
    ],
)
