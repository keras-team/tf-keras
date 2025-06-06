# Description:
#   Implementation of TF-Keras benchmarks.

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")
# Placeholder: load unaliased py_library

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

py_library(
    name = "saved_model_benchmark_util",
    srcs = ["saved_model_benchmark_util.py"],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "densenet_benchmark_test",
    srcs = ["densenet_benchmark_test.py"],
    tags = [
        "no_pip",  # b/161253163
        "no_windows",  # b/160628318
    ],
    deps = [
        ":saved_model_benchmark_util",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "efficientnet_benchmark_test",
    srcs = ["efficientnet_benchmark_test.py"],
    tags = [
        "no_pip",  # b/161253163
        "no_windows",  # b/160628318
    ],
    deps = [
        ":saved_model_benchmark_util",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "inception_resnet_v2_benchmark_test",
    srcs = ["inception_resnet_v2_benchmark_test.py"],
    tags = [
        "no_pip",  # b/161253163
        "no_windows",  # b/160628318
    ],
    deps = [
        ":saved_model_benchmark_util",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "mobilenet_benchmark_test",
    srcs = ["mobilenet_benchmark_test.py"],
    tags = [
        "no_pip",  # b/161253163
        "no_windows",  # b/160628318
    ],
    deps = [
        ":saved_model_benchmark_util",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "nasnet_large_benchmark_test",
    srcs = ["nasnet_large_benchmark_test.py"],
    tags = [
        "no_pip",  # b/161253163
        "no_windows",  # b/160628318
    ],
    deps = [
        ":saved_model_benchmark_util",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "resnet152_v2_benchmark_test",
    srcs = ["resnet152_v2_benchmark_test.py"],
    tags = [
        "no_pip",  # b/161253163
        "no_windows",  # b/160628318
    ],
    deps = [
        ":saved_model_benchmark_util",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "vgg_benchmark_test",
    srcs = ["vgg_benchmark_test.py"],
    tags = [
        "no_pip",  # b/161253163
        "no_windows",  # b/160628318
    ],
    deps = [
        ":saved_model_benchmark_util",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "xception_benchmark_test",
    srcs = ["xception_benchmark_test.py"],
    tags = [
        "no_pip",  # b/161253163
        "no_windows",  # b/160628318
    ],
    deps = [
        ":saved_model_benchmark_util",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)
