# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Description:
#   TF-Keras saving and loading files for SavedModel.

# buildifier: disable=same-origin-load

load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")
load("@rules_python//python:py_binary.bzl", "py_binary")
load("@rules_python//python:py_library.bzl", "py_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras/layers/rnn:__pkg__",
        "//tf_keras/saving:__subpackages__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "order_preserving_set",
    srcs = ["order_preserving_set.py"],
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/engine:base_layer_utils",
        "//tf_keras/utils:layer_utils",
    ],
)

py_library(
    name = "saved_model",
    srcs = [
        "__init__.py",
        "base_serialization.py",
        "constants.py",
        "json_utils.py",
        "layer_serialization.py",
        "load.py",
        "metric_serialization.py",
        "model_serialization.py",
        "network_serialization.py",
        "save.py",
        "save_impl.py",
        "serialized_attributes.py",
    ],
    deps = [
        ":order_preserving_set",
        ":utils",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/utils:generic_utils",
    ],
)

tf_py_test(
    name = "revive_test",
    size = "medium",
    srcs = ["revive_test.py"],
    shard_count = 8,
    tags = [
        "no_windows",  # b/158005583
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "json_utils_test",
    size = "small",
    srcs = ["json_utils_test.py"],
    deps = [
        ":saved_model",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "saved_model_test",
    size = "medium",
    srcs = ["saved_model_test.py"],
    shard_count = 4,
    tags = [
        "no_oss",  # TODO(keras-team): Fails in OSS.
        "no_pip",  # TODO(b/202022379)
        "no_rocm",
        "no_windows",
        "notsan",  #TODO(b/181771982): it is flaky
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

py_binary(
    name = "create_test_saved_model",
    srcs = ["create_test_saved_model.py"],
    tags = ["no_oss"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:regularizers",
        "//tf_keras/testing_infra:test_utils",
        "//third_party/py/absl/flags",
        "@pypi//absl_py",  # absl:app
    ],
)

tf_py_test(
    name = "determinism_test",
    srcs = ["determinism_test.py"],
    data = [":create_test_saved_model.par"],
    tags = ["no_oss"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)
