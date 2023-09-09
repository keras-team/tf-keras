package(default_visibility = ["//tf_keras:__subpackages__"])

# Description:
#  Tools for building the TensorFlow pip package.

COMMON_PIP_DEPS = [
    "//tf_keras/api:keras_api",
    # The following targets are not included by //tf_keras:keras,
    # eg to avoid circular dependency with TF, but they should still be included
    # in the PIP package.
    "//tf_keras/legacy_tf_layers:convolutional",
    "//tf_keras/legacy_tf_layers:core",
    "//tf_keras/legacy_tf_layers:layers_base",
    "//tf_keras/legacy_tf_layers:normalization",
    "//tf_keras/legacy_tf_layers:pooling",
    "//tf_keras/layers/rnn:legacy_cell_wrappers",
    "//tf_keras/layers/rnn:legacy_cells",
    "//tf_keras/optimizers:legacy_learning_rate_decay",
    # Need to include testing libraries in pip package so our pip
    # release tests can run. (see py_test rule in keras.bzl for more context).
    # Essentially, everything needed to run the test (except the test file itself)
    # must be contained in the pip package since we strip away all deps.
    "//tf_keras/testing_infra:test_combinations",
    "//tf_keras/testing_infra:test_utils",
    "//tf_keras/benchmarks:keras_benchmark_lib_pip",
    "//tf_keras/dtensor:integration_test_utils",
    "//tf_keras/dtensor:test_util",
    "//tf_keras/distribute:distribute_test_lib_pip",
    "//tf_keras/integration_test:preprocessing_test_utils",
    "//tf_keras/integration_test/models:models",
    "//tf_keras/layers/preprocessing:preprocessing_test_utils",
    "//tf_keras/layers/preprocessing/benchmarks:feature_column_benchmark",
    "//tf_keras/mixed_precision:test_util",
    "//tf_keras/tests:model_architectures",
    "//tf_keras/tests:model_subclassing_test_util",
    "//tf_keras/utils:dataset_creator",
    "//tf_keras/utils:kpl_test_utils",
]

sh_binary(
    name = "build_pip_package",
    srcs = ["build_pip_package.sh"],
    data = COMMON_PIP_DEPS,
)
