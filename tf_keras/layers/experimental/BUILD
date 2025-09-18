# Description:
# DynamicEmbeddingLayer allows for the continuous updating of the vocabulary and embeddings during
# the training process.

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "distribute_py_test")  # buildifier: disable=same-origin-load
load("@rules_python//python:py_library.bzl", "py_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//third_party/py/keras:license"],
    default_visibility = [
        "//tf_keras:friends",
    ],
    licenses = ["notice"],
)

py_library(
    name = "dynamic_lookup",
    srcs = [
        "__init__.py",
        "dynamic_lookup.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/layers",
    ],
)

tf_py_test(
    name = "dynamic_lookup_test",
    size = "small",
    srcs = ["dynamic_lookup_test.py"],
    shard_count = 6,
    tags = ["notpu"],
    deps = [
        ":dynamic_lookup",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

py_library(
    name = "dynamic_embedding",
    srcs = ["dynamic_embedding.py"],
    deps = [
        ":dynamic_lookup",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
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
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
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
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:callbacks",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
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
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
        "@pypi//portpicker",
    ],
)
