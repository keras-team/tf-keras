# Build and test tf_keras artifacts using Bazel commands.

## Build tf_keras artifacts

There are 3 types of `tf_keras` artifacts: self-built, nightly and release.
The repository environment variables that control which type of the artifact
should be built are described
[here](https://github.com/openxla/xla/blob/05cd3e6bfbfa3ab8a2441f873eb9966a5497b10c/third_party/py/python_wheel.bzl#L116-L131)

To build the artifacts using Bazel, use the following command:

```
# Upgrade requirements lock file
bazel run requirements.update --repo_env=HERMETIC_PYTHON_VERSION=3.10 -- --upgrade

# Build the artifact
TAG_FILTERS="-no_oss,-oss_excluded,-oss_serial,-gpu,-benchmark-test,-no_oss_py3,-no_pip,-nopip"
bazel build \
  --repo_env=HERMETIC_PYTHON_VERSION=3.10 \
  --build_tag_filters="${TAG_FILTERS}" \
  ${BUILD_OPTIONS} \
  -- \
  ${TARGET_NAME}
```

The target name is `//tf_keras/wheel:tf_keras_wheel` for the wheel and
`//tf_keras/wheel:tf_keras_source_package` for the source package.

The build options examples:
1. Self-built artifacts:
`BUILD_OPTIONS=""`

2. Nightly artifacts:
`BUILD_OPTIONS=--repo_env=ML_WHEEL_TYPE=nightly --repo_env=ML_WHEEL_BUILD_DATE=$(date +%Y%m%d%H)`

3. Release artifacts:
`BUILD_OPTIONS=--repo_env=ML_WHEEL_TYPE=release`

4. Release candidate artifacts:
`BUILD_OPTIONS=--repo_env=ML_WHEEL_TYPE=release --repo_env=ML_WHEEL_VERSION_SUFFIX=rc1`

The resulting artifacts will be located in `bazel-bin/tf_keras/wheel/dist` dir.

## Test pre-built tf_keras wheels

Hermetic Python can install the wheels provided in the `dist` folder inside the
cloned GitHub repository (this feature is configured by
`python_init_repositories` call in the `WORKSPACE`). Before running the tests,
one should copy `tf_keras` wheel inside the `dist` folder.

Additional wheel requirements for the self-built and release builds:
`tensorflow` and `keras` wheels (`keras` is required by `tensorflow`) should be
placed in the `dist` folder as well.

The testing of nightly `tf_keras` wheels doesn't require this
procedure, because the `requirements_lock_3_10.txt` file has lock information for
`tf-nightly` and `keras-nightly` wheels.

Note that the wheels in the `dist` folder have priority over the versions
provided in the lock file, e.g. if `tf_nightly` wheel is placed inside `dist`
folder, then hermetic Python will use that wheel instead of the `tf_nightly`
version specified in the lock file.

The command to test the pre-built wheels:

```
TAG_FILTERS="-no_oss,-oss_excluded,-oss_serial,-gpu,-benchmark-test,-no_oss_py3,-no_pip,-nopip"

# Wheel sanity test
bazel test \
  --repo_env=HERMETIC_PYTHON_VERSION=3.10 \
  --build_tag_filters="${TAG_FILTERS}" \
  ${BUILD_OPTIONS} \
  -- \
  //tf_keras/wheel:pypi_tf_keras_wheel_test

# Convert local test files to refer to tf_keras.src.x instead of tf_keras.x
python3 -c "import pip_build;pip_build.convert_keras_imports('tf_keras')"

bazel test \
    --repo_env=HERMETIC_PYTHON_VERSION=3.10 \
    --test_timeout 300,450,1200,3600 \
    --test_output=errors \
    --keep_going \
    --build_tag_filters="${TAG_FILTERS}" \
    --test_tag_filters="${TAG_FILTERS}" \
    --define=no_keras_py_deps=true \
    --build_tests_only \
    ${BUILD_OPTIONS} \
    -- //tf_keras/... -//tf_keras/integration_test/...
```

Note that `$BUILD_OPTIONS` should be the same as were used for building
`tf_keras` wheel.