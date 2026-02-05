# Description:
#   Contains the TF-Keras preprocess layers (internal TensorFlow version).

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "distribute_py_test")  # buildifier: disable=same-origin-load
load("@rules_python//python:py_library.bzl", "py_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/tools/pip_package:__pkg__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "preprocessing",
    srcs = [
        "__init__.py",
    ],
    strict_deps = False,
    deps = [
        ":discretization",
        ":hashed_crossing",
        ":hashing",
        ":image_preprocessing",
        ":integer_lookup",
        ":normalization",
        ":preprocessing_stage",
        ":preprocessing_test_utils",
        ":string_lookup",
        ":text_vectorization",
    ],
)

py_library(
    name = "discretization",
    srcs = [
        "discretization.py",
    ],
    strict_deps = False,
    deps = [
        ":preprocessing_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine",
        "//tf_keras/utils:tf_utils",
        "@pypi//numpy",
    ],
)

py_library(
    name = "hashing",
    srcs = [
        "hashing.py",
    ],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine",
        "@pypi//numpy",
    ],
)

py_library(
    name = "hashed_crossing",
    srcs = [
        "hashed_crossing.py",
    ],
    strict_deps = False,
    deps = [
        ":preprocessing_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:base_preprocessing_layer",
        "//tf_keras/utils:layer_utils",
    ],
)

py_library(
    name = "image_preprocessing",
    srcs = [
        "image_preprocessing.py",
    ],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine",
        "//tf_keras/engine:input_spec",
        "//tf_keras/preprocessing:image",
        "//tf_keras/utils:image_utils",
        "//tf_keras/utils:tf_utils",
        "@pypi//numpy",
    ],
)

py_library(
    name = "index_lookup",
    srcs = [
        "index_lookup.py",
    ],
    strict_deps = False,
    deps = [
        ":category_encoding",
        ":preprocessing_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine",
        "@pypi//numpy",
    ],
)

py_library(
    name = "normalization",
    srcs = [
        "normalization.py",
    ],
    strict_deps = False,
    deps = [
        ":preprocessing_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine",
        "@pypi//numpy",
    ],
)

py_library(
    name = "integer_lookup",
    srcs = [
        "integer_lookup.py",
    ],
    strict_deps = False,
    deps = [
        ":index_lookup",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine",
    ],
)

py_library(
    name = "text_vectorization",
    srcs = [
        "text_vectorization.py",
    ],
    strict_deps = False,
    deps = [
        ":category_encoding",
        ":preprocessing_utils",
        ":string_lookup",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine",
        "//tf_keras/utils:layer_utils",
        "//tf_keras/utils:tf_utils",
        "@pypi//numpy",
    ],
)

py_library(
    name = "category_encoding",
    srcs = [
        "category_encoding.py",
    ],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/engine",
        "//tf_keras/engine:input_spec",
        "//tf_keras/utils:layer_utils",
        "@pypi//numpy",
    ],
)

py_library(
    name = "string_lookup",
    srcs = [
        "string_lookup.py",
    ],
    strict_deps = False,
    deps = [
        ":index_lookup",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine",
    ],
)

py_library(
    name = "preprocessing_stage",
    srcs = [
        "preprocessing_stage.py",
    ],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine",
        "//tf_keras/utils:tf_utils",
        "@pypi//numpy",
    ],
)

py_library(
    name = "preprocessing_test_utils",
    srcs = ["preprocessing_test_utils.py"],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "@pypi//numpy",
    ],
)

py_library(
    name = "preprocessing_utils",
    srcs = ["preprocessing_utils.py"],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "preprocessing_utils_test",
    srcs = ["preprocessing_utils_test.py"],
    deps = [
        ":preprocessing_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/utils:generic_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

tf_py_test(
    name = "category_encoding_test",
    srcs = ["category_encoding_test.py"],
    deps = [
        ":category_encoding",
        ":preprocessing_test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/utils:generic_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

distribute_py_test(
    name = "category_encoding_distribution_test",
    srcs = ["category_encoding_distribution_test.py"],
    disable_mlir_bridge = False,
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    main = "category_encoding_distribution_test.py",
    shard_count = 4,
    tags = [
        "multi_and_single_gpu",
        "no_oss",  # b/189866692
        "noguitar",  # b/190034522
        "nomultivm",  # TODO(b/170502145)
    ],
    tpu_tags = [
        "no_oss",  # b/155502591
    ],
    deps = [
        ":category_encoding",
        ":preprocessing_test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras:backend",
        "//tf_keras/distribute:strategy_combinations",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

distribute_py_test(
    name = "image_preprocessing_distribution_test",
    srcs = ["image_preprocessing_distribution_test.py"],
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    main = "image_preprocessing_distribution_test.py",
    shard_count = 4,
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
        "notpu",  # TODO(b/210148622)
    ],
    tpu_tags = [
        "no_oss",
        "noguitar",  # TODO(b/183957207)
    ],
    deps = [
        ":image_preprocessing",
        ":preprocessing_test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/distribute:strategy_combinations",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//portpicker",
    ],
)

tf_py_test(
    name = "discretization_test",
    srcs = ["discretization_test.py"],
    shard_count = 4,
    tags = ["no_rocm"],
    deps = [
        ":discretization",
        ":preprocessing_test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

distribute_py_test(
    name = "discretization_distribution_test",
    srcs = ["discretization_distribution_test.py"],
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    main = "discretization_distribution_test.py",
    shard_count = 4,
    tags = [
        "multi_and_single_gpu",
        "no_oss",  # TODO(b/189956080)
        "noguitar",  # b/190034522
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":discretization",
        ":preprocessing_test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/distribute:strategy_combinations",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "hashing_test",
    srcs = ["hashing_test.py"],
    shard_count = 4,
    deps = [
        ":hashing",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/engine",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

distribute_py_test(
    name = "hashing_distribution_test",
    srcs = ["hashing_distribution_test.py"],
    disable_mlir_bridge = False,
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    main = "hashing_distribution_test.py",
    shard_count = 4,
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":hashing",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/distribute:strategy_combinations",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//portpicker",
    ],
)

tf_py_test(
    name = "hashed_crossing_test",
    srcs = ["hashed_crossing_test.py"],
    shard_count = 4,
    deps = [
        ":hashing",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/engine",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "index_lookup_test",
    srcs = ["index_lookup_test.py"],
    shard_count = 4,
    tags = ["noasan"],  # TODO(b/183961255)
    deps = [
        ":index_lookup",
        ":preprocessing_test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/utils:generic_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

distribute_py_test(
    name = "index_lookup_distribution_test",
    srcs = ["index_lookup_distribution_test.py"],
    disable_mlir_bridge = False,
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    main = "index_lookup_distribution_test.py",
    shard_count = 4,
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
    ],
    tpu_tags = ["no_oss"],
    deps = [
        ":index_lookup",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/distribute:strategy_combinations",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//portpicker",
    ],
)

cuda_py_test(
    name = "image_preprocessing_test",
    srcs = ["image_preprocessing_test.py"],
    shard_count = 4,
    tags = [
        "no_windows",  # TODO(b/184424727): Re-enable this.
    ],
    deps = [
        ":image_preprocessing",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/engine",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:generic_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "normalization_test",
    srcs = ["normalization_test.py"],
    shard_count = 4,
    tags = [
        "noasan",  # TODO(b/337374867) fails with -fsanitize=null
    ],
    deps = [
        ":normalization",
        ":preprocessing_test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

tf_py_test(
    name = "integer_lookup_test",
    srcs = ["integer_lookup_test.py"],
    tags = ["noasan"],  # TODO(b/183961255)
    deps = [
        ":integer_lookup",
        ":preprocessing_test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/utils:generic_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

distribute_py_test(
    name = "normalization_distribution_test",
    srcs = ["normalization_distribution_test.py"],
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    main = "normalization_distribution_test.py",
    shard_count = 8,
    tags = [
        "no_oss",
        "nomultivm",  # TODO(b/170502145)
    ],
    deps = [
        ":normalization",
        ":preprocessing_test_utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/distribute:strategy_combinations",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "text_vectorization_test",
    srcs = ["text_vectorization_test.py"],
    shard_count = 4,
    deps = [
        ":preprocessing_test_utils",
        ":text_vectorization",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/utils:generic_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

distribute_py_test(
    name = "text_vectorization_distribution_test",
    srcs = ["text_vectorization_distribution_test.py"],
    disable_mlir_bridge = False,
    env = {
        "CUDA_MODULE_LOADING": "LAZY",
    },
    main = "text_vectorization_distribution_test.py",
    shard_count = 8,
    tags = [
        "multi_and_single_gpu",
        "nomultivm",  # TODO(b/170502145)
    ],
    tpu_tags = [
        "no_oss",  # b/155502591
    ],
    deps = [
        ":preprocessing_test_utils",
        ":text_vectorization",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/distribute:strategy_combinations",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//portpicker",
    ],
)

tf_py_test(
    name = "string_lookup_test",
    srcs = ["string_lookup_test.py"],
    tags = [
        "notsan",  #b/168758821
    ],
    deps = [
        ":preprocessing_test_utils",
        ":string_lookup",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/utils:generic_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

tf_py_test(
    name = "preprocessing_stage_test",
    srcs = ["preprocessing_stage_test.py"],
    tags = ["no_windows"],  # TODO(b/152991402)
    deps = [
        ":preprocessing_stage",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)
