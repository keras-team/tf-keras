# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
#   Contains the TF-Keras Mixed Precision API (TensorFlow version).

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")  # buildifier: disable=same-origin-load
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@rules_python//python:py_library.bzl", "py_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        # TODO(scottzhu): Remove these two deps and convert the test to integration test.
        "//third_party/tensorflow/python/distribute:__pkg__",  # For collective_all_reduce_strategy_test
        "//tf_keras:friends",
        "//third_party/tensorflow/tools/pip_package:__pkg__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "mixed_precision_experimental",
    srcs = ["__init__.py"],
    deps = [
        ":loss_scale_optimizer",
        ":policy",
    ],
)

py_library(
    name = "policy",
    srcs = [
        "policy.py",
    ],
    deps = [
        ":device_compatibility_check",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

tf_py_test(
    name = "policy_test",
    size = "medium",
    srcs = [
        "policy_test.py",
    ],
    tags = ["no_rocm"],
    deps = [
        ":policy",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

py_library(
    name = "device_compatibility_check",
    srcs = ["device_compatibility_check.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
    ],
)

cuda_py_test(
    name = "device_compatibility_check_test",
    srcs = ["device_compatibility_check_test.py"],
    deps = [
        ":device_compatibility_check",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
    ],
)

py_library(
    name = "autocast_variable",
    srcs = [
        "autocast_variable.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/distribute",
    ],
)

tf_py_test(
    name = "autocast_variable_test",
    size = "medium",
    srcs = ["autocast_variable_test.py"],
    deps = [
        ":autocast_variable",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/layers",
        "//tf_keras/optimizers/legacy:optimizers",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

py_library(
    name = "loss_scale_optimizer",
    srcs = ["loss_scale_optimizer.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/utils:generic_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

cuda_py_test(
    name = "loss_scale_optimizer_test",
    size = "medium",
    srcs = ["loss_scale_optimizer_test.py"],
    shard_count = 4,
    deps = [
        ":loss_scale_optimizer",
        ":test_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
    ],
)

cuda_py_test(
    name = "mixed_precision_graph_rewrite_test",
    size = "small",
    srcs = ["mixed_precision_graph_rewrite_test.py"],
    deps = [
        ":loss_scale_optimizer",
        ":policy",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/optimizers/legacy:optimizers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

py_library(
    name = "test_util",
    srcs = ["test_util.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
    ],
)

cuda_py_test(
    name = "layer_test",
    size = "medium",
    srcs = ["layer_test.py"],
    tags = [
        "no_pip",
        "no_windows",  # b/139083295: bfloat16 tests fail on Windows
    ],
    deps = [
        ":test_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

cuda_py_test(
    name = "model_test",
    size = "medium",
    srcs = ["model_test.py"],
    data = [
        "//tf_keras/mixed_precision/testdata:lso_ckpt_tf2.2",
        "//tf_keras/mixed_precision/testdata:lso_savedmodel_tf2.2",
    ],
    shard_count = 5,
    tags = [
        "no_pip",
        "no_windows",  # b/139083295: bfloat16 tests fail on Windows
    ],
    deps = [
        ":test_util",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)

cuda_py_test(
    name = "layer_correctness_test",
    size = "medium",
    srcs = ["layer_correctness_test.py"],
    shard_count = 10,
    tags = [
        "no_rocm",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
    ],
)
