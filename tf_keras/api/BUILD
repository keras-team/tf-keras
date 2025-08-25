# Description:
# Package for TF-Keras.

# Placeholder: load unaliased py_binary
# Placeholder: load unaliased py_library
load("//tf_keras/api:api_gen.bzl", "generate_apis")
load("//tf_keras/api:api_init_files.bzl", "KERAS_API_INIT_FILES", "KERAS_API_INIT_FILES_V1")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/py/tensorflow:__subpackages__",
    ],
    licenses = ["notice"],  # Apache 2.0 License
)

# The target used by PIP package which need to generate API init files during OSS build.
py_library(
    name = "tf_keras_api",
    srcs = [
        ":tf_keras_python_api_gen",
        ":tf_keras_python_api_gen_compat_v1",
        ":tf_keras_python_api_gen_compat_v2",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
    ],
)

py_binary(
    name = "extractor_wrapper",
    srcs = ["extractor_wrapper.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/tensorflow/python/tools/api/generator2/extractor"
        "@pypi//absl_py",  # absl:app
    ],
)

py_binary(
    name = "generator_wrapper",
    srcs = ["generator_wrapper.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/tensorflow/python/tools/api/generator2/generator"
        "@pypi//absl_py",  # absl:app
    ],
)

generate_apis(
    name = "tf_keras_python_api_gen",
    api_version = 1,
    output_files = KERAS_API_INIT_FILES_V1,
    output_package = "tf_keras.api",
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        # "//third_party/tensorflow/lite/python:analyzer",
        # "//third_party/tensorflow/lite/python:lite",
        # "//third_party/tensorflow/lite/python/authoring",
    ],
)

generate_apis(
    name = "tf_keras_python_api_gen_compat_v1",
    api_version = 1,
    output_dir = "_v1/",
    output_files = KERAS_API_INIT_FILES_V1,
    output_package = "tf_keras.api._v1",
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        # "//third_party/tensorflow/lite/python:analyzer",
        # "//third_party/tensorflow/lite/python:lite",
        # "//third_party/tensorflow/lite/python/authoring",
    ],
)

generate_apis(
    name = "tf_keras_python_api_gen_compat_v2",
    api_version = 2,
    output_dir = "_v2/",
    output_files = KERAS_API_INIT_FILES,
    output_package = "tf_keras.api._v2",
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        # "//third_party/tensorflow/lite/python:analyzer",
        # "//third_party/tensorflow/lite/python:lite",
        # "//third_party/tensorflow/lite/python/authoring",
    ],
)
