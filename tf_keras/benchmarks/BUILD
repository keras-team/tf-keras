# Description:
#   Implementation of TF-Keras benchmarks.

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")
# Placeholder: load unaliased py_binary
# Placeholder: load unaliased py_library
# Placeholder: load unaliased py_test

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = ["//visibility:public"],
    licenses = ["notice"],
)

# To run CPU benchmarks:
#   bazel run -c opt benchmarks_test -- --benchmarks=.

# To run GPU benchmarks:
#   bazel run --config=cuda -c opt --copt="-mavx" benchmarks_test -- \
#     --benchmarks=.

# To run a subset of benchmarks using --benchmarks flag.
# --benchmarks: the list of benchmarks to run. The specified value is interpreted
# as a regular expression and any benchmark whose name contains a partial match
# to the regular expression is executed.
# e.g. --benchmarks=".*lstm*." will run all lstm layer related benchmarks.

# Add all benchmarks related utils here for pip testing dependencies.
py_library(
    name = "keras_benchmark_lib_pip",
    deps = [
        ":benchmark_util",
        ":distribution_util",
        "//tf_keras/benchmarks/saved_model_benchmarks:saved_model_benchmark_util",
    ],
)

# This lib is mainly for running benchmarks on mlcompass infra.
py_library(
    name = "profiler_lib",
    visibility = [
        "//learning/brain/contrib/keras_benchmark:__subpackages__",
        "//tf_keras:friends",
    ],
)

COMMON_TAGS = [
    "no_pip",  # b/161253163
    "no_windows",  # b/160628318
]

py_test(
    name = "keras_cpu_benchmark_test",
    size = "large",
    srcs = ["keras_cpu_benchmark_test.py"],
    tags = COMMON_TAGS,
    deps = [
        ":benchmark_util",
        ":profiler_lib",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/api:tf_keras_api",
        "@pypi//numpy",
    ],
)

cuda_py_test(
    name = "eager_microbenchmarks_test",
    size = "medium",
    srcs = ["eager_microbenchmarks_test.py"],
    tags = COMMON_TAGS + [
        "no_oss_py38",  # TODO(b/162044699)
    ],
    deps = [
        ":profiler_lib",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/utils:tf_inspect",
    ],
)

cuda_py_test(
    name = "model_components_benchmarks_test",
    srcs = ["model_components_benchmarks_test.py"],
    deps = [
        ":profiler_lib",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/api:tf_keras_api",
    ],
)

py_library(
    name = "benchmark_util",
    srcs = [
        "__init__.py",
        "benchmark_util.py",
    ],
    deps = [
        ":distribution_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/api:tf_keras_api",
        "@pypi//numpy",
    ],
)

py_test(
    name = "benchmark_util_test",
    srcs = ["benchmark_util_test.py"],
    tags = COMMON_TAGS,
    deps = [
        ":benchmark_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/api:tf_keras_api",
    ],
)

py_library(
    name = "distribution_util",
    srcs = ["distribution_util.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
    ],
)

py_test(
    name = "optimizer_benchmarks_test",
    srcs = ["optimizer_benchmarks_test.py"],
    tags = COMMON_TAGS + [
        "no_oss_py38",  # TODO(b/162044699)
    ],
    deps = [
        ":benchmark_util",
        ":profiler_lib",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/optimizers/legacy:optimizers",
    ],
)

# Run memory profiler on TF-Keras model.
# Please make sure `memory_profiler` is installed.
# To run the memory profiler:
# With CPU:
#   bazel run -c opt model_memory_profile -- --model=YOUR_MODEL_NAME
# With GPU:
#   bazel run -c opt --config=cuda model_memory_profile -- --model=YOUR_MODEL_NAME
py_binary(
    name = "model_memory_profile",
    srcs = ["model_memory_profile.py"],
    tags = ["no_oss"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
    ],
)

py_test(
    name = "metrics_memory_benchmark_test",
    srcs = ["metrics_memory_benchmark_test.py"],
    tags = COMMON_TAGS,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/api:tf_keras_api",
        "@pypi//numpy",
    ],
)
