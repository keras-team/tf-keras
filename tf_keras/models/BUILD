# TF-Keras models

# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "distribute_py_test")  # buildifier: disable=same-origin-load

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
    ],
    licenses = ["notice"],
)

py_library(
    name = "sharpness_aware_minimization",
    srcs = ["sharpness_aware_minimization.py"],
    deps = [
        ":cloning",
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:data_adapter",
    ],
)

py_library(
    name = "models",
    srcs = [
        "__init__.py",
    ],
    deps = [
        ":cloning",
        ":sharpness_aware_minimization",
    ],
)

py_library(
    name = "cloning",
    srcs = [
        "cloning.py",
    ],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/engine",
        "//tf_keras/engine:base_layer",
        "//tf_keras/metrics",
        "//tf_keras/optimizers",
        "//tf_keras/saving",
        "//tf_keras/utils:generic_utils",
        "//tf_keras/utils:version_utils",
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
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
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
        ":sharpness_aware_minimization",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/optimizers",
        "//tf_keras/testing_infra:test_combinations",
    ],
)
