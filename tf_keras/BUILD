# Description:
#   Contains the TF-Keras API (internal TensorFlow version).

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
load("@rules_python//python:py_library.bzl", "py_library")

# copybara:uncomment_begin(google-only)
# load("//tools/build_defs/license:license.bzl", "license")
# copybara:uncomment_end

package(
    # copybara:uncomment default_applicable_licenses = [":license"],
    default_visibility = [":friends"],
    licenses = ["notice"],
)

# TF-Keras code that doesn't live in core TF-Keras directory, but still
# need to directly access the keras code.
# We shouldn't add any client side package to this list.
package_group(
    name = "friends",
    packages = ["//tf_keras/..."],
)

exports_files(["LICENSE"])

config_setting(
    name = "no_keras_py_deps",
    define_values = {"no_keras_py_deps": "true"},
    visibility = ["//visibility:public"],
)

py_library(
    name = "tf_keras",
    srcs = [
        "__init__.py",
    ],
    deps = [
        ":backend",
        ":engine",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/applications",
        "//tf_keras/datasets",
        "//tf_keras/distribute",
        "//tf_keras/estimator",
        "//tf_keras/feature_column",
        "//tf_keras/layers",
        "//tf_keras/layers/rnn:legacy_cell_wrappers",
        "//tf_keras/layers/rnn:legacy_cells",
        "//tf_keras/legacy_tf_layers:layers",
        "//tf_keras/mixed_precision:mixed_precision_experimental",
        "//tf_keras/models",
        "//tf_keras/optimizers",
        "//tf_keras/premade_models",
        "//tf_keras/preprocessing",
        "//tf_keras/saving",
        "//tf_keras/testing_infra:keras_doctest_lib",
        "//tf_keras/testing_infra:test_utils",  # For keras.__internal__ API
        "//tf_keras/utils",
        "@pypi//h5py",
        "@pypi//numpy",
        "@pypi//pydot",
        "@pypi//pyyaml",
        "@pypi//scipy",
    ],
)

py_library(
    name = "backend",
    srcs = ["backend.py"],
    deps = [
        ":backend_config",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/distribute:distribute_coordinator_utils",
        "//tf_keras/engine:keras_tensor",
        "//tf_keras/utils:control_flow_util",
        "//tf_keras/utils:object_identity",
        "//tf_keras/utils:tf_contextlib",
        "//tf_keras/utils:tf_inspect",
        "@pypi//numpy",
    ],
)

py_library(
    name = "backend_config",
    srcs = ["backend_config.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

# TODO(scottzhu): Cleanup this target and point all the user to keras/engine.
py_library(
    name = "engine",
    srcs = [
        "//tf_keras/metrics",
        "//tf_keras/models",
    ],
    deps = [
        "//tf_keras/engine",
    ],
)

py_library(
    name = "activations",
    srcs = [
        "activations.py",
    ],
    deps = [
        ":backend",
        "//tf_keras/layers/activation",
        "//tf_keras/utils:engine_utils",
    ],
)

# TODO(scottzhu): Cleanup this target and point all the user to keras/engine.
py_library(
    name = "base_layer",
    srcs = [],
    deps = [
        "//tf_keras/engine:base_layer",
    ],
)

py_library(
    name = "callbacks",
    srcs = [
        "callbacks.py",
    ],
    deps = [
        ":backend",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/distribute:distributed_file_utils",
        "//tf_keras/distribute:worker_training_state",
        "//tf_keras/protobuf:projector_config_proto_py_pb2",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:mode_keys",
        "//tf_keras/utils:timed_threads",
        "@pypi//tensorboard_data_server",
    ],
)

py_library(
    name = "callbacks_v1",
    srcs = [
        "callbacks_v1.py",
    ],
    deps = [
        ":backend",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/utils:engine_utils",
        "@pypi//tensorboard_data_server",
    ],
)

py_library(
    name = "constraints",
    srcs = [
        "constraints.py",
    ],
    deps = [
        ":backend",
        "//tf_keras/utils:engine_utils",
    ],
)

py_library(
    name = "losses",
    srcs = [
        "losses.py",
    ],
    deps = [
        ":backend",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/saving:saving_lib",
        "//tf_keras/utils:engine_utils",
        "//tf_keras/utils:generic_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

py_library(
    name = "regularizers",
    srcs = [
        "regularizers.py",
    ],
    deps = [
        ":backend",
        "//tf_keras/utils:engine_utils",
    ],
)

# Internally urllib.request.urlretrieve library requires Google
# SSL context to be provided to work in python 3. This isn't needed in OSS.
# copybara:uncomment_begin(google-only)
# py_library(
#     name = "url_utils",
#     srcs = ["google/url_utils.py"],
#     deps = ["//pyglib/contrib/google_ssl"],
# )
# copybara:uncomment_end

# Some tf.distribute related feature requires detecting platform.
# Internally we'd like to recognize Borg, which is not needed in OSS.
# copybara:uncomment_begin(google-only)
# py_library(
#     name = "distribute_utils",
#     srcs = ["google/distribute_utils.py"],
#     deps = [
#         "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
#         "//third_party/py/requests",
#         "@pypi//six",
#     ],
# )
# copybara:uncomment_end

tf_py_test(
    name = "activations_test",
    size = "small",
    srcs = ["activations_test.py"],
    deps = [
        ":activations",
        ":backend",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/layers",
        "//tf_keras/layers/activation",
        "//tf_keras/layers/core",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
        "@pypi//scipy",
    ],
)

tf_py_test(
    name = "constraints_test",
    size = "small",
    srcs = ["constraints_test.py"],
    deps = [
        ":backend",
        ":constraints",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "regularizers_test",
    size = "medium",
    srcs = ["regularizers_test.py"],
    deps = [
        ":tf_keras",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

tf_py_test(
    name = "losses_test",
    size = "small",
    srcs = ["losses_test.py"],
    shard_count = 4,
    tags = [
        "noasan",  # b/186128525
    ],
    deps = [
        ":backend",
        ":losses",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/utils:engine_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "callbacks_test",
    size = "medium",
    srcs = ["callbacks_test.py"],
    shard_count = 6,
    tags = [
        "no_pip",  # TODO(b/276923757)
        "no_tfrt",  # TODO(b/179690526)
        "notsan",
    ],
    deps = [
        ":tf_keras",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "callbacks_v1_test",
    size = "medium",
    srcs = ["callbacks_v1_test.py"],
    tags = [
        "nomac",  # Using profiler causes segfault in MacOS runs.
        "notsan",
    ],
    deps = [
        ":callbacks",
        ":callbacks_v1",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine",
        "//tf_keras/layers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:np_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "backend_test",
    size = "medium",
    srcs = ["backend_test.py"],
    shard_count = 4,
    deps = [
        ":backend",
        ":engine",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
        "@pypi//scipy",
    ],
)

tf_py_test(
    name = "backend_config_test",
    size = "medium",
    srcs = ["backend_config_test.py"],
    deps = [
        ":backend",
        ":backend_config",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
    ],
)

# copybara:uncomment_begin(google-only)
# tf_py_test(
#     name = "url_utils_test",
#     srcs = ["google/url_utils_test.py"],
#     deps = [
#         ":url_utils",
#         "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
#         "//testing/pymocks:matchers",
#     ],
# )
#
# tf_py_test(
#     name = "distribute_utils_test",
#     srcs = ["google/distribute_utils_test.py"],
#     deps = [
#         ":distribute_utils",
#         "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
#         "//testing/pymocks:matchers",
#         "//tf_keras/distribute",
#     ],
# )
#
# license(
#     name = "license",
#     package_name = "tf_keras",
# )
# copybara:uncomment_end
