# TensorFlow API backwards compatibility tests.

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = ["//tf_keras/api:__subpackages__"],
    licenses = ["notice"],  # Apache 2.0
)

exports_files([
    "README.txt",
    "API_UPDATE_WARNING.txt",
])

tf_py_test(
    name = "api_compatibility_test",
    srcs = ["api_compatibility_test.py"],
    data = [
        "//tf_keras/api/golden:api_golden_v1",
        "//tf_keras/api/golden:api_golden_v2",
        "//tf_keras/api/tests:API_UPDATE_WARNING.txt",
        "//tf_keras/api/tests:README.txt",
    ],
    tags = [
        "DO_NOT_USE_MIGRATION_ONLY_NO_PYTHON_NEXT",
        "no_oss",  # TODO(scottzhu): Fix this in OSS test.
        "no_pip",
        "no_rocm",
        "no_windows",  # Bugs due to some paths.
    ],
    deps = [
        "//:expect_six_installed",
        "//third_party/py/tensorflow",
        "//third_party/tensorflow/python/lib/io:file_io",
        "//third_party/tensorflow/tools/api/lib:python_object_to_proto_visitor",
        "//third_party/tensorflow/tools/common:public_api",
        "//third_party/tensorflow/tools/common:traverse",
    ],
)
