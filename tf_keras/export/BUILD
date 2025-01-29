# Description:
#   Contains the TF-Keras save model API (internal TensorFlow version).

# Placeholder: load unaliased py_library
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    # TODO(scottzhu): Remove non-keras deps from TF.
    default_visibility = [
        "//tf_keras:friends",
    ],
    licenses = ["notice"],
)

py_library(
    name = "export_lib",
    srcs = [
        "export_lib.py",
    ],
    deps = [
        "//:expect_tensorflow_installed",
    ],
)

tf_py_test(
    name = "export_lib_test",
    size = "medium",
    srcs = ["export_lib_test.py"],
    deps = [
        ":export_lib",
        "//:expect_absl_installed",  # absl/testing:parameterized
        "//:expect_tensorflow_installed",
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)
