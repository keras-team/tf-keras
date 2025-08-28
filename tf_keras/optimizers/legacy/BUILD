# Description:
#   Contains the TF-Keras OptimizerV2 API (internal TensorFlow version).

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")
# Placeholder: load unaliased py_library

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    # TODO(scottzhu): Remove non-keras deps from TF.
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/cc/saved_model:__pkg__",  # For unit tests.
    ],
    licenses = ["notice"],
)

py_library(
    name = "optimizers",
    srcs = [
        "__init__.py",
        "adadelta.py",
        "adagrad.py",
        "adam.py",
        "adamax.py",
        "ftrl.py",
        "gradient_descent.py",
        "nadam.py",
        "optimizer_v2.py",
        "rmsprop.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras:backend_config",
        "//tf_keras/engine:base_layer_utils",
        "//tf_keras/initializers",
        "//tf_keras/optimizers:utils",
        "//tf_keras/optimizers/schedules:learning_rate_schedule",
        "//tf_keras/utils:layer_utils",
        "//tf_keras/utils:tf_utils",
    ],
)

cuda_py_test(
    name = "adagrad_test",
    size = "medium",
    srcs = ["adagrad_test.py"],
    shard_count = 4,
    deps = [
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "adam_test",
    size = "medium",
    srcs = ["adam_test.py"],
    shard_count = 4,
    tags = [
        "no_rocm",
        "no_windows",  # TODO(b/171384138)
    ],
    deps = [
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "adamax_test",
    size = "medium",
    srcs = ["adamax_test.py"],
    shard_count = 4,
    # TODO(b/168527439): invalid resource variable reference on GPU for TFRT.
    tags = ["no_rocm"],
    deps = [
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "adadelta_test",
    size = "medium",
    srcs = ["adadelta_test.py"],
    shard_count = 4,
    # TODO(b/168527439): invalid resource variable reference on GPU for TFRT.
    deps = [
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "ftrl_test",
    size = "medium",
    srcs = ["ftrl_test.py"],
    shard_count = 4,
    deps = [
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

cuda_py_test(
    name = "gradient_descent_test",
    size = "medium",
    srcs = ["gradient_descent_test.py"],
    shard_count = 4,
    deps = [
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "nadam_test",
    size = "medium",
    srcs = ["nadam_test.py"],
    shard_count = 4,
    deps = [
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

cuda_py_test(
    name = "optimizer_v2_test",
    size = "medium",
    srcs = ["optimizer_v2_test.py"],
    shard_count = 8,
    tags = [
        "no_windows",
    ],
    deps = [
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

cuda_py_test(
    name = "rmsprop_test",
    size = "medium",
    srcs = ["rmsprop_test.py"],
    shard_count = 2,
    # TODO(b/168527439): invalid resource variable reference on GPU for TFRT.
    deps = [
        ":optimizers",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)
