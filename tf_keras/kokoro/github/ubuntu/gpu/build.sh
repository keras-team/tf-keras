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

nvidia-smi

cd "${KOKORO_ROOT}/"

cd "src/github/tf-keras"

TF_CUDA_COMPUTE_CAPABILITIES="sm_60,sm_70,sm_80,sm_89,compute_90"

tag_filters="gpu,-no_gpu,-nogpu,-benchmark-test,-no_oss,-oss_excluded,-oss_serial,-no_gpu_presubmit"
# There are only 4 GPU available on the local test machine.
TF_GPU_COUNT=4
TF_TESTS_PER_GPU=8
LOCAL_TEST_JOBS=32  # TF_GPU_COUNT * TF_TESTS_PER_GPU

bazel run requirements.update --repo_env=HERMETIC_PYTHON_VERSION=3.9 -- --upgrade
bazel test --test_timeout 300,600,1200,3600 --test_output=errors --keep_going \
   --repo_env=HERMETIC_PYTHON_VERSION=3.9 \
   --build_tests_only \
   --repo_env=TF_CUDA_COMPUTE_CAPABILITIES="${TF_CUDA_COMPUTE_CAPABILITIES}" \
   --repo_env=HERMETIC_CUDA_VERSION=12.5.1 \
   --repo_env=HERMETIC_CUDNN_VERSION=9.3.0 \
   --config=cuda \
   --test_env=TF_GPU_COUNT=${TF_GPU_COUNT} \
   --test_env=TF_TESTS_PER_GPU=${TF_TESTS_PER_GPU} \
   --build_tag_filters="${tag_filters}" \
   --test_tag_filters="${tag_filters}" \
   --run_under=@org_keras//tf_keras/tools/gpu_build:parallel_gpu_execute \
   --local_test_jobs=${LOCAL_TEST_JOBS} \
   -- //tf_keras/...
