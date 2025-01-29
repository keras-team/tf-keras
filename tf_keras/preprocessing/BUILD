# Description:
#   Contains the TF-Keras preprocessing layers (internal TensorFlow version).

# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")

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
    deps = [
        "//:expect_numpy_installed",
        "//:expect_pillow_installed",
        "//:expect_scipy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras:backend",
        "//tf_keras/utils:data_utils",
        "//tf_keras/utils:image_utils",
    ],
)

py_library(
    name = "sequence",
    srcs = [
        "sequence.py",
    ],
    deps = [
        "//:expect_tensorflow_installed",
        "//tf_keras/utils:data_utils",
    ],
)

py_library(
    name = "text",
    srcs = [
        "text.py",
    ],
    deps = ["//:expect_tensorflow_installed"],
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
        "//:expect_numpy_installed",
        "//:expect_pandas_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "sequence_test",
    size = "small",
    srcs = ["sequence_test.py"],
    deps = [
        ":sequence",
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

tf_py_test(
    name = "text_test",
    size = "small",
    srcs = ["text_test.py"],
    deps = [
        ":text",
        "//:expect_numpy_installed",
        "//:expect_tensorflow_installed",
        "//tf_keras/testing_infra:test_combinations",
    ],
)
