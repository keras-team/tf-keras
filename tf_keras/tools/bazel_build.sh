#!/bin/bash
BAZEL_VERSION=7.4.1
rm -rf ~/bazel
mkdir ~/bazel

pushd ~/bazel
wget https://github.com/bazelbuild/bazel/releases/download/"${BAZEL_VERSION}"/bazel-"${BAZEL_VERSION}"-installer-linux-x86_64.sh
chmod +x bazel-*.sh
./bazel-"${BAZEL_VERSION}"-installer-linux-x86_64.sh --user
rm bazel-"${BAZEL_VERSION}"-installer-linux-x86_64.sh
popd

PATH="/home/kbuilder/bin:$PATH"
which bazel
bazel version

TAG_FILTERS="-no_oss,-oss_excluded,-oss_serial,-gpu,-benchmark-test,-no_oss_py3,-no_pip,-nopip"
bazel run requirements.update --repo_env=HERMETIC_PYTHON_VERSION=3.9 -- --upgrade
bazel build \
    --repo_env=HERMETIC_PYTHON_VERSION=3.9 \
    --build_tag_filters="${TAG_FILTERS}" \
    -- //tf_keras/...
