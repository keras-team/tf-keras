# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/python/feature_column:__subpackages__",  # For unit testing
        "//third_party/tensorflow/python/tpu:__subpackages__",  # For unit testing
    ],
    licenses = ["notice"],
)

py_library(
    name = "feature_column",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
    deps = [
        ":base_feature_layer",
        ":dense_features",
        ":dense_features_v2",
        ":sequence_feature_column",
    ],
)

py_library(
    name = "base_feature_layer",
    srcs = ["base_feature_layer.py"],
    srcs_version = "PY3",
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/engine:base_layer",
        "//tf_keras/utils:generic_utils",
    ],
)

py_library(
    name = "dense_features",
    srcs = [
        "dense_features.py",
    ],
    srcs_version = "PY3",
    deps = [
        ":base_feature_layer",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
    ],
)

py_library(
    name = "dense_features_v2",
    srcs = [
        "dense_features_v2.py",
    ],
    srcs_version = "PY3",
    deps = [
        ":base_feature_layer",
        ":dense_features",
        "//:expect_tensorflow_installed",
        "//tf_keras/utils:tf_contextlib",
    ],
)

tf_py_test(
    name = "dense_features_test",
    srcs = ["dense_features_test.py"],
    tags = ["no_pip"],
    deps = [
        ":dense_features",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "dense_features_v2_test",
    srcs = ["dense_features_v2_test.py"],
    tags = ["no_pip"],
    deps = [
        ":dense_features_v2",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

py_library(
    name = "sequence_feature_column",
    srcs = ["sequence_feature_column.py"],
    srcs_version = "PY3",
    deps = [
        ":base_feature_layer",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
    ],
)

tf_py_test(
    name = "sequence_feature_column_test",
    srcs = ["sequence_feature_column_test.py"],
    deps = [
        ":sequence_feature_column",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "sequence_feature_column_integration_test",
    srcs = ["sequence_feature_column_integration_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    tags = ["no_pip"],
    deps = [
        ":dense_features",
        ":sequence_feature_column",
        "//:expect_tensorflow_installed",
        "//tf_keras/layers/core",
        "//tf_keras/layers/merging",
        "//tf_keras/layers/rnn",
        "//tf_keras/metrics",  # Import it here since base_layer didn't import it due to circular dependency.
    ],
)
