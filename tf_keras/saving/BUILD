# Description:
#   Contains the TF-Keras save model API (internal TensorFlow version).

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
# Placeholder: load unaliased py_library

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    # TODO(scottzhu): Remove non-keras deps from TF.
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/python/distribute:__pkg__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "saving",
    srcs = [
        "__init__.py",
        "legacy/hdf5_format.py",
        "legacy/model_config.py",
        "legacy/save.py",
        "legacy/saving_utils.py",
        "pickle_utils.py",
        "saving_api.py",
    ],
    deps = [
        ":object_registration",
        ":serialization",
        ":serialization_lib",
        "//:expect_h5py_installed",
        "//:expect_tensorflow_installed",
        "//:expect_yaml_installed",
        "//tf_keras:backend",
        "//tf_keras:losses",
        "//tf_keras:regularizers",
        "//tf_keras/engine:input_spec",
        "//tf_keras/mixed_precision:autocast_variable",
        "//tf_keras/optimizers",
        "//tf_keras/protobuf:saved_metadata_proto_py_pb2",
        "//tf_keras/saving/legacy/saved_model",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:metrics_utils",
        "//tf_keras/utils:mode_keys",
    ],
)

py_library(
    name = "saving_lib",
    srcs = [
        "saving_lib.py",
    ],
    deps = [
        ":serialization_lib",
        "//:expect_tensorflow_installed",
        "//tf_keras/utils:generic_utils",
        "//tf_keras/utils:io_utils",
    ],
)

tf_py_test(
    name = "saving_lib_test",
    size = "medium",
    srcs = ["saving_lib_test.py"],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/utils:generic_utils",
    ],
)

py_library(
    name = "object_registration",
    srcs = [
        "object_registration.py",
    ],
)

py_library(
    name = "serialization_lib",
    srcs = [
        "serialization_lib.py",
    ],
    deps = [
        ":object_registration",
        ":serialization",
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/saving/legacy/saved_model:utils",
    ],
)

py_library(
    name = "serialization",
    srcs = [
        "legacy/serialization.py",
    ],
    deps = [
        ":object_registration",
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/utils:tf_contextlib",
        "//tf_keras/utils:tf_inspect",
    ],
)

tf_py_test(
    name = "object_registration_test",
    size = "small",
    srcs = ["object_registration_test.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras",
    ],
)

tf_py_test(
    name = "metrics_serialization_test",
    size = "medium",
    srcs = ["legacy/metrics_serialization_test.py"],
    shard_count = 8,
    tags = [
        "notsan",  # TODO(b/170870790)
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "losses_serialization_test",
    size = "medium",
    srcs = ["legacy/losses_serialization_test.py"],
    shard_count = 4,
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "pickle_utils_test",
    size = "medium",
    srcs = ["pickle_utils_test.py"],
    shard_count = 4,
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "save_weights_test",
    size = "medium",
    srcs = ["legacy/save_weights_test.py"],
    shard_count = 4,
    tags = [
        "no_oss_py35",  # b/147011479
        "no_pip",  # TODO(b/202022379)
        "no_windows",
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "save_test",
    size = "medium",
    srcs = ["legacy/save_test.py"],
    shard_count = 4,
    tags = [
        "no_pip",  # TODO(b/202022379)
    ],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "saving_utils_test",
    size = "medium",
    srcs = ["legacy/saving_utils_test.py"],
    tags = ["notsan"],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "serialization_lib_test",
    size = "small",
    srcs = ["serialization_lib_test.py"],
    deps = [
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/saving:serialization",
        "//tf_keras/testing_infra:test_combinations",
    ],
)
