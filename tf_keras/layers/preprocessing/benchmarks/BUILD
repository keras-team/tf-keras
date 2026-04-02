# Benchmarks for TF-Keras preprocessing layers.
load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@rules_python//python:py_library.bzl", "py_library")

package(
    default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/tools/pip_package:__pkg__",
    ],
    licenses = ["notice"],
)

tf_py_test(
    name = "category_encoding_benchmark",
    srcs = ["category_encoding_benchmark.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:category_encoding",
        "//third_party/py/tensorflow:tensorflow_core",
    ],
)

tf_py_test(
    name = "hashing_benchmark",
    srcs = ["hashing_benchmark.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:hashing",
        "//third_party/py/tensorflow:tensorflow_core",
    ],
)

tf_py_test(
    name = "index_lookup_adapt_benchmark",
    srcs = ["index_lookup_adapt_benchmark.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:index_lookup",
        "//third_party/py/tensorflow:tensorflow_core",
    ],
)

tf_py_test(
    name = "index_lookup_forward_benchmark",
    srcs = ["index_lookup_forward_benchmark.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:index_lookup",
        "//third_party/py/tensorflow:tensorflow_core",
    ],
)

tf_py_test(
    name = "normalization_adapt_benchmark",
    srcs = ["normalization_adapt_benchmark.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:normalization",
        "//third_party/py/tensorflow:tensorflow_core",
    ],
)

tf_py_test(
    name = "discretization_adapt_benchmark",
    srcs = ["discretization_adapt_benchmark.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:discretization",
        "//third_party/py/tensorflow:tensorflow_core",
    ],
)

cuda_py_test(
    name = "image_preproc_benchmark",
    srcs = ["image_preproc_benchmark.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:image_preprocessing",
        "//third_party/py/tensorflow:tensorflow_core",
    ],
)

tf_py_test(
    name = "bucketized_column_dense_benchmark",
    srcs = ["bucketized_column_dense_benchmark.py"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:discretization",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "hashed_crossing_benchmark",
    srcs = ["hashed_crossing_benchmark.py"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:hashed_crossing",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "category_hash_dense_benchmark",
    srcs = ["category_hash_dense_benchmark.py"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:hashing",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "category_hash_varlen_benchmark",
    srcs = ["category_hash_varlen_benchmark.py"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:hashing",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "category_vocab_file_dense_benchmark",
    srcs = ["category_vocab_file_dense_benchmark.py"],
    tags = ["no_windows"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:string_lookup",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "category_vocab_file_varlen_benchmark",
    srcs = ["category_vocab_file_varlen_benchmark.py"],
    tags = ["no_windows"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:string_lookup",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "category_vocab_list_dense_benchmark",
    srcs = ["category_vocab_list_dense_benchmark.py"],
    tags = ["no_windows"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:string_lookup",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "category_vocab_list_indicator_dense_benchmark",
    srcs = ["category_vocab_list_indicator_dense_benchmark.py"],
    tags = ["no_windows"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:category_encoding",
        "//tf_keras/layers/preprocessing:string_lookup",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "category_vocab_list_indicator_varlen_benchmark",
    srcs = ["category_vocab_list_indicator_varlen_benchmark.py"],
    tags = ["no_windows"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:category_encoding",
        "//tf_keras/layers/preprocessing:string_lookup",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "category_vocab_list_varlen_benchmark",
    srcs = ["category_vocab_list_varlen_benchmark.py"],
    tags = ["no_windows"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//tf_keras/layers/preprocessing:string_lookup",
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "embedding_dense_benchmark",
    srcs = ["embedding_dense_benchmark.py"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

tf_py_test(
    name = "embedding_varlen_benchmark",
    srcs = ["embedding_varlen_benchmark.py"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)

py_library(
    name = "feature_column_benchmark",
    srcs = [
        "__init__.py",
        "feature_column_benchmark.py",
    ],
    # copybara:uncomment strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        "//third_party/py/tensorflow:tensorflow_core",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "weighted_embedding_varlen_benchmark",
    srcs = ["weighted_embedding_varlen_benchmark.py"],
    deps = [
        ":feature_column_benchmark",
        "//third_party/py/tensorflow:tensorflow_core",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_no_contrib"
        # "//third_party/tensorflow/python/eager:def_function",
    ],
)
