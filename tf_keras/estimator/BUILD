# Description:
#   Contains TF-Keras models to Estimator converter

load("@rules_python//python:py_library.bzl", "py_library")

package(
    default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
    ],
    licenses = ["notice"],
)

py_library(
    name = "estimator",
    srcs = [
        "__init__.py",
    ],
    strict_deps = False,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)
