# Description:
#   Contains the TF-Keras preprocessing layers (internal TensorFlow version).

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
load("@rules_python//python:py_library.bzl", "py_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
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
        ":image",
        ":sequence",
        ":text",
        "//tf_keras/utils",
    ],
)

py_library(
    name = "image",
    srcs = [
        "image.py",
    ],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:backend",
        "//tf_keras/utils:data_utils",
        "//tf_keras/utils:image_utils",
        "@pypi//numpy",
        "@pypi//pillow",
        "@pypi//scipy",
    ],
)

py_library(
    name = "sequence",
    srcs = [
        "sequence.py",
    ],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/utils:data_utils",
    ],
)

py_library(
    name = "text",
    srcs = [
        "text.py",
    ],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

tf_py_test(
    name = "image_test",
    size = "medium",
    srcs = ["image_test.py"],
    tags = [
        "no_oss",  # TODO(scottzhu): Fix for multiple export issue.
    ],
    deps = [
        ":image",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
        "@pypi//pandas",
    ],
)

tf_py_test(
    name = "sequence_test",
    size = "small",
    srcs = ["sequence_test.py"],
    deps = [
        ":sequence",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "text_test",
    size = "small",
    srcs = ["text_test.py"],
    deps = [
        ":text",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)
