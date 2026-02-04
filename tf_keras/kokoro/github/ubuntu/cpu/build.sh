#!/bin/bash
# Copyright 2020 Google Inc. All Rights Reserved.
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

set -e
set -x

cd "${KOKORO_ROOT}/"

cd "src/github/tf-keras"

bazel run requirements.update --repo_env=HERMETIC_PYTHON_VERSION=3.10 -- --upgrade
bazel test --test_timeout 300,450,1200,3600 --test_output=errors --keep_going \
   --repo_env=HERMETIC_PYTHON_VERSION=3.10 \
   --build_tests_only \
   --build_tag_filters="-no_oss,-oss_excluded" \
   --test_tag_filters="-no_oss,-oss_excluded" \
   -- //tf_keras/...