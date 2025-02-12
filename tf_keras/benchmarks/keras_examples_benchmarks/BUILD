# Description:
#   Implementation of TF-Keras benchmarks.

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")

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

COMMON_TAGS = [
    "no_pip",  # b/161253163
    "no_windows",  # b/160628318
]

cuda_py_test(
    name = "bidirectional_lstm_benchmark_test",
    srcs = ["bidirectional_lstm_benchmark_test.py"],
    python_version = "PY3",
    tags = COMMON_TAGS,
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:benchmark_util",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "text_classification_transformer_benchmark_test",
    srcs = ["text_classification_transformer_benchmark_test.py"],
    python_version = "PY3",
    tags = COMMON_TAGS,
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:benchmark_util",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "antirectifier_benchmark_test",
    srcs = ["antirectifier_benchmark_test.py"],
    python_version = "PY3",
    tags = COMMON_TAGS,
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:benchmark_util",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "mnist_conv_benchmark_test",
    srcs = ["mnist_conv_benchmark_test.py"],
    python_version = "PY3",
    tags = COMMON_TAGS,
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:benchmark_util",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "mnist_hierarchical_rnn_benchmark_test",
    srcs = ["mnist_hierarchical_rnn_benchmark_test.py"],
    python_version = "PY3",
    tags = COMMON_TAGS,
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:benchmark_util",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "mnist_irnn_benchmark_test",
    srcs = ["mnist_irnn_benchmark_test.py"],
    python_version = "PY3",
    tags = COMMON_TAGS,
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:benchmark_util",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "reuters_mlp_benchmark_test",
    srcs = ["reuters_mlp_benchmark_test.py"],
    python_version = "PY3",
    tags = COMMON_TAGS,
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:benchmark_util",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "cifar10_cnn_benchmark_test",
    srcs = ["cifar10_cnn_benchmark_test.py"],
    python_version = "PY3",
    tags = COMMON_TAGS,
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:benchmark_util",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)

cuda_py_test(
    name = "mnist_conv_custom_training_benchmark_test",
    srcs = ["mnist_conv_custom_training_benchmark_test.py"],
    python_version = "PY3",
    tags = COMMON_TAGS,
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/api:tf_keras_api",
        "//tf_keras/benchmarks:benchmark_util",
        "//tf_keras/benchmarks:distribution_util",
        "//tf_keras/benchmarks:profiler_lib",
    ],
)
