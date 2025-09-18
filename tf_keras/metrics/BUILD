# Copyright 2022 The TensorFlow Authors. All Rights Reserved.
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
#   Contains the TF-Keras metrics submodule.

load("@org_keras//tf_keras:tf_keras.bzl", "cuda_py_test")
load("@org_keras//tf_keras:tf_keras.bzl", "tf_py_test")  # buildifier: disable=same-origin-load
load("@rules_python//python:py_library.bzl", "py_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//tf_keras:license"],
    default_visibility = [
        "//tf_keras:friends",
        "//third_party/tensorflow/python/feature_column:__subpackages__",
        "//third_party/tensorflow/python/tpu:__subpackages__",
        "//third_party/tensorflow_estimator:__subpackages__",
    ],
    licenses = ["notice"],
)

py_library(
    name = "metrics",
    srcs = [
        "__init__.py",
        "accuracy_metrics.py",
        "base_metric.py",
        "confusion_metrics.py",
        "f_score_metrics.py",
        "hinge_metrics.py",
        "iou_metrics.py",
        "probabilistic_metrics.py",
        "py_metric.py",
        "regression_metrics.py",
    ],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras:activations",
        "//tf_keras:backend",
        "//tf_keras:losses",
        "//tf_keras/distribute",
        "//tf_keras/dtensor",
        "//tf_keras/dtensor:utils",
        "//tf_keras/engine:base_layer",
        "//tf_keras/engine:base_layer_utils",
        "//tf_keras/utils:generic_utils",
        "//tf_keras/utils:metrics_utils",
        "//tf_keras/utils:tf_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "metrics_functional_test",
    size = "small",
    srcs = ["metrics_functional_test.py"],
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "accuracy_metrics_test",
    size = "medium",
    srcs = ["accuracy_metrics_test.py"],
    shard_count = 4,
    deps = [
        ":metrics",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "confusion_metrics_test",
    size = "medium",
    srcs = ["confusion_metrics_test.py"],
    shard_count = 4,
    deps = [
        ":metrics",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/models",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "//tf_keras/utils:metrics_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
        "@pypi//scipy",
    ],
)

tf_py_test(
    name = "f_score_metrics_test",
    size = "medium",
    srcs = ["f_score_metrics_test.py"],
    shard_count = 4,
    deps = [
        ":metrics",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "hinge_metrics_test",
    size = "medium",
    srcs = ["hinge_metrics_test.py"],
    shard_count = 4,
    deps = [
        ":metrics",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "iou_metrics_test",
    size = "medium",
    srcs = ["iou_metrics_test.py"],
    shard_count = 4,
    deps = [
        ":metrics",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "probabilistic_metrics_test",
    size = "medium",
    srcs = ["probabilistic_metrics_test.py"],
    shard_count = 4,
    deps = [
        ":metrics",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "regression_metrics_test",
    size = "medium",
    srcs = ["regression_metrics_test.py"],
    shard_count = 4,
    deps = [
        ":metrics",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "base_metric_test",
    size = "medium",
    srcs = ["base_metric_test.py"],
    shard_count = 4,
    deps = [
        ":metrics",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
        "@pypi//numpy",
    ],
)

tf_py_test(
    name = "metrics_correctness_test",
    size = "medium",
    srcs = ["metrics_correctness_test.py"],
    shard_count = 4,
    deps = [
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/testing_infra:test_combinations",
        "@pypi//absl_py",  # absl/testing:parameterized
        "@pypi//numpy",
    ],
)

cuda_py_test(
    name = "py_metric_test",
    size = "medium",
    srcs = ["py_metric_test.py"],
    shard_count = 2,
    tags = [
        "no_windows",
    ],
    deps = [
        ":metrics",
        "//:tf_nightly_with_deps",  # "//third_party/py/tensorflow:tensorflow_core"
        "//tf_keras",
        "//tf_keras/layers",
        "//tf_keras/testing_infra:test_combinations",
        "//tf_keras/testing_infra:test_utils",
    ],
)
