# This package contains all the DTensor related TF-Keras components.
# Since DTensor is not a public API yet, all the DTensor related change
# can't be exposed to public yet.

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
load("@rules_python//python:py_library.bzl", "py_library")

# copybara:uncomment_begin(google-only)
# load(
#     "//third_party/tensorflow/dtensor:build_defs.bzl",
#     "dtensor_test",
# )
# copybara:uncomment_end

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//learning/brain/distribute/experimental/auto_distribute:__pkg__",
        "//learning/brain/distribute/python:__subpackages__",
        "//learning/brain/experimental/dtensor/models:__subpackages__",
        "//tf_keras:friends",
    ],
    licenses = ["notice"],
)

py_library(
    name = "dtensor",
    srcs = ["__init__.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

tf_py_test(
    name = "initializers_test",
    srcs = ["initializers_test.py"],
    shard_count = 4,
    deps = [
        ":dtensor",
        ":test_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/initializers",
        "//tf_keras/utils:tf_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "layers_test",
    srcs = ["layers_test.py"],
    shard_count = 4,
    tags = ["no_oss"],
    deps = [
        ":dtensor",
        ":test_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/layers",
        "//tf_keras/utils:tf_utils",
        "@pypi//numpy",
    ],
)

py_library(
    name = "layout_map",
    srcs = ["layout_map.py"],
    deps = [
        ":dtensor",
        ":lazy_variable",
        ":utils",
        "//tf_keras/engine:base_layer",
    ],
)

tf_py_test(
    name = "layout_map_test",
    srcs = ["layout_map_test.py"],
    tags = ["no_oss"],
    deps = [
        ":dtensor",
        ":layout_map",
        ":test_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/utils:tf_utils",
        "@pypi//numpy",
    ],
)

py_library(
    name = "integration_test_utils",
    srcs = ["integration_test_utils.py"],
    deps = [
        ":dtensor",
        ":layout_map",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:losses",
        "//tf_keras/datasets",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/utils:np_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "metrics_test",
    srcs = ["metrics_test.py"],
    shard_count = 4,
    deps = [
        ":dtensor",
        ":test_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/metrics",
        "//tf_keras/utils:tf_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

# copybara:uncomment_begin(google-only)
# dtensor_test(
#     name = "mnist_model_test",
#     srcs = ["mnist_model_test.py"],
#     env = {
#         "CUDA_MODULE_LOADING": "LAZY",
#         "TF_GPU_ALLOCATOR": "cuda_malloc_async",
#     },
#     tags = [
#         "no_oss",
#         "requires-net:external",
#     ],
#     deps = [
#         ":dtensor",
#         ":integration_test_utils",
#         ":layout_map",
#         ":test_util",
#         "@pypi//numpy",
#         "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
#         "//tf_keras:backend",
#         "//tf_keras/optimizers",
#         "//tf_keras/utils:tf_utils",
#     ],
# )
# copybara:uncomment_end

tf_py_test(
    name = "optimizers_test",
    srcs = ["optimizers_test.py"],
    deps = [
        ":dtensor",
        ":layout_map",
        ":test_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:losses",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/optimizers",
        "@pypi//numpy",
    ],
)

py_library(
    name = "lazy_variable",
    srcs = ["lazy_variable.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    deps = [
        ":dtensor",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

tf_py_test(
    name = "utils_test",
    srcs = ["utils_test.py"],
    deps = [
        ":dtensor",
        ":test_util",
        ":utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/layers",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

py_library(
    name = "test_util",
    srcs = ["test_util.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "save_load_test",
    srcs = ["save_load_test.py"],
    deps = [
        ":dtensor",
        ":layout_map",
        ":test_util",
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/utils:tf_utils",
    ],
)

# copybara:uncomment_begin(google-only)
# dtensor_test(
#     name = "strategy_integration_test",
#     srcs = ["strategy_integration_test.py"],
#     shard_count = {
#         "CPU": 2,
#         "GPU": 4,
#         "TPU": 2,
#     },
#     tags = ["no_oss"],
#     deps = [
#         ":integration_test_utils",
#         ":test_util",
#         "@pypi//absl_py",  # absl/testing:parameterized
#         "@pypi//numpy",
#         "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
#         "//tf_keras:backend",
#         "//tf_keras/mixed_precision:mixed_precision_experimental",
#         "//tf_keras/optimizers",
#         "//tf_keras/utils:tf_utils",
#         "//third_party/tensorflow/dtensor/python/tests:test_util",
#         "//third_party/tensorflow/python/distribute/experimental:mirrored_strategy",
#     ],
# )
# copybara:uncomment_end
