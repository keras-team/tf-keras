# Description:
#   Contains the TF-Keras datasets package (internal TensorFlow version).

# Placeholder: load unaliased py_library

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
    ],
    licenses = ["notice"],
)

py_library(
    name = "datasets",
    srcs = [
        "__init__.py",
        "boston_housing.py",
        "cifar.py",
        "cifar10.py",
        "cifar100.py",
        "fashion_mnist.py",
        "imdb.py",
        "mnist.py",
        "reuters.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/utils:engine_utils",
    ],
)
