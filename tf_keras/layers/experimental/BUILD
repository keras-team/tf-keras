# Description:
# DynamicEmbeddingLayer allows for the continuous updating of the vocabulary and embeddings during
# the training process.

# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
load("@org_keras//tf_keras:tf_keras.bzl", "distribute_py_test")

package(
    # copybara:uncomment default_applicable_licenses = ["//third_party/py/keras:license"],
    default_visibility = [
        "//tf_keras:friends",
    ],
    licenses = ["notice"],
)

py_library(
    name = "dynamic_lookup",
    srcs = ["dynamic_lookup.py"],
    srcs_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/layers",
    ],
)

tf_py_test(
    name = "dynamic_lookup_test",
    size = "small",
    srcs = ["dynamic_lookup_test.py"],
    python_version = "PY3",
    shard_count = 6,
    tags = ["notpu"],
    deps = [
        ":dynamic_lookup",
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

py_library(
    name = "dynamic_embedding",
    srcs = ["dynamic_embedding.py"],
    deps = [
        ":dynamic_lookup",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/utils",
    ],
)

tf_py_test(
    name = "dynamic_embedding_test",
    srcs = ["dynamic_embedding_test.py"],
    tags = ["notpu"],
    deps = [
        ":dynamic_embedding",
        "//:expect_tensorflow_installed",
        "//tf_keras:callbacks",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)

distribute_py_test(
    name = "dynamic_embedding_distributed_test",
    srcs = ["dynamic_embedding_distributed_test.py"],
    tags = [
        "no_oss",
        "no_windows",
        "nomultivm",
        "notpu",
    ],
    deps = [
        ":dynamic_embedding",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras:callbacks",
        "//tf_keras/testing_infra:test_utils",
    ],
)

distribute_py_test(
    name = "dynamic_lookup_distributed_test",
    srcs = ["dynamic_lookup_distributed_test.py"],
    tags = [
        "nomultivm",
        "notpu",
    ],
    deps = [
        ":dynamic_lookup",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_utils",
    ],
)
