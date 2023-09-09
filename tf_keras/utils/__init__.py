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
"""Public TF-Keras utilities."""

# isort: off

# Serialization related
from tf_keras.saving.serialization_lib import deserialize_keras_object
from tf_keras.saving.serialization_lib import serialize_keras_object
from tf_keras.saving.object_registration import CustomObjectScope
from tf_keras.saving.object_registration import custom_object_scope
from tf_keras.saving.object_registration import get_custom_objects
from tf_keras.saving.object_registration import get_registered_name
from tf_keras.saving.object_registration import register_keras_serializable

# Dataset related
from tf_keras.utils.audio_dataset import audio_dataset_from_directory
from tf_keras.utils.text_dataset import text_dataset_from_directory
from tf_keras.utils.timeseries_dataset import timeseries_dataset_from_array
from tf_keras.utils.image_dataset import image_dataset_from_directory
from tf_keras.utils.dataset_utils import split_dataset

# Sequence related
from tf_keras.utils.data_utils import GeneratorEnqueuer
from tf_keras.utils.data_utils import OrderedEnqueuer
from tf_keras.utils.data_utils import Sequence
from tf_keras.utils.data_utils import SequenceEnqueuer

# Image related
from tf_keras.utils.image_utils import array_to_img
from tf_keras.utils.image_utils import img_to_array
from tf_keras.utils.image_utils import load_img
from tf_keras.utils.image_utils import save_img

# Python utils
from tf_keras.utils.tf_utils import set_random_seed
from tf_keras.utils.generic_utils import Progbar
from tf_keras.utils.data_utils import get_file

# Preprocessing utils
from tf_keras.utils.feature_space import FeatureSpace

# Internal
from tf_keras.utils.layer_utils import get_source_inputs
from tf_keras.utils.layer_utils import warmstart_embedding_matrix

# Deprecated
from tf_keras.utils.np_utils import normalize
from tf_keras.utils.np_utils import to_categorical
from tf_keras.utils.np_utils import to_ordinal
from tf_keras.utils.data_utils import pad_sequences

# Evaluation related
from tf_keras.utils.sidecar_evaluator import SidecarEvaluator
from tf_keras.utils.sidecar_evaluator import SidecarEvaluatorModelExport

# Timed Thread
from tf_keras.utils.timed_threads import TimedThread

# Visualization related
from tf_keras.utils.vis_utils import model_to_dot
from tf_keras.utils.vis_utils import plot_model
