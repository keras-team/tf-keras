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
"""Integration tests for TF-Keras applications."""

import os

import tensorflow.compat.v2 as tf
from absl.testing import parameterized

from tf_keras import backend
from tf_keras import utils
from tf_keras.applications import convnext
from tf_keras.applications import densenet
from tf_keras.applications import efficientnet
from tf_keras.applications import efficientnet_v2
from tf_keras.applications import inception_resnet_v2
from tf_keras.applications import inception_v3
from tf_keras.applications import mobilenet
from tf_keras.applications import mobilenet_v2
from tf_keras.applications import mobilenet_v3
from tf_keras.applications import nasnet
from tf_keras.applications import regnet
from tf_keras.applications import resnet
from tf_keras.applications import resnet_rs
from tf_keras.applications import resnet_v2
from tf_keras.applications import vgg16
from tf_keras.applications import vgg19
from tf_keras.applications import xception
from tf_keras.testing_infra import test_utils

MODEL_LIST_NO_NASNET = [
    (resnet.ResNet50, 2048),
    (resnet.ResNet101, 2048),
    (resnet.ResNet152, 2048),
    (resnet_v2.ResNet50V2, 2048),
    (resnet_v2.ResNet101V2, 2048),
    (resnet_v2.ResNet152V2, 2048),
    (vgg16.VGG16, 512),
    (vgg19.VGG19, 512),
    (xception.Xception, 2048),
    (inception_v3.InceptionV3, 2048),
    (inception_resnet_v2.InceptionResNetV2, 1536),
    (mobilenet.MobileNet, 1024),
    (mobilenet_v2.MobileNetV2, 1280),
    (mobilenet_v3.MobileNetV3Small, 576),
    (mobilenet_v3.MobileNetV3Large, 960),
    (convnext.ConvNeXtTiny, 768),
    (convnext.ConvNeXtSmall, 768),
    (convnext.ConvNeXtBase, 1024),
    (convnext.ConvNeXtLarge, 1536),
    (convnext.ConvNeXtXLarge, 2048),
    (densenet.DenseNet121, 1024),
    (densenet.DenseNet169, 1664),
    (densenet.DenseNet201, 1920),
    (efficientnet.EfficientNetB0, 1280),
    (efficientnet.EfficientNetB1, 1280),
    (efficientnet.EfficientNetB2, 1408),
    (efficientnet.EfficientNetB3, 1536),
    (efficientnet.EfficientNetB4, 1792),
    (efficientnet.EfficientNetB5, 2048),
    (efficientnet.EfficientNetB6, 2304),
    (efficientnet.EfficientNetB7, 2560),
    (efficientnet_v2.EfficientNetV2B0, 1280),
    (efficientnet_v2.EfficientNetV2B1, 1280),
    (efficientnet_v2.EfficientNetV2B2, 1408),
    (efficientnet_v2.EfficientNetV2B3, 1536),
    (efficientnet_v2.EfficientNetV2S, 1280),
    (efficientnet_v2.EfficientNetV2M, 1280),
    (efficientnet_v2.EfficientNetV2L, 1280),
    (regnet.RegNetX002, 368),
    (regnet.RegNetX004, 384),
    (regnet.RegNetX006, 528),
    (regnet.RegNetX008, 672),
    (regnet.RegNetX016, 912),
    (regnet.RegNetX032, 1008),
    (regnet.RegNetX040, 1360),
    (regnet.RegNetX064, 1624),
    (regnet.RegNetX080, 1920),
    (regnet.RegNetX120, 2240),
    (regnet.RegNetX160, 2048),
    (regnet.RegNetX320, 2520),
    (regnet.RegNetY002, 368),
    (regnet.RegNetY004, 440),
    (regnet.RegNetY006, 608),
    (regnet.RegNetY008, 768),
    (regnet.RegNetY016, 888),
    (regnet.RegNetY032, 1512),
    (regnet.RegNetY040, 1088),
    (regnet.RegNetY064, 1296),
    (regnet.RegNetY080, 2016),
    (regnet.RegNetY120, 2240),
    (regnet.RegNetY160, 3024),
    (regnet.RegNetY320, 3712),
    (resnet_rs.ResNetRS50, 2048),
    (resnet_rs.ResNetRS101, 2048),
    (resnet_rs.ResNetRS152, 2048),
    (resnet_rs.ResNetRS200, 2048),
    (resnet_rs.ResNetRS270, 2048),
    (resnet_rs.ResNetRS350, 2048),
    (resnet_rs.ResNetRS420, 2048),
]

NASNET_LIST = [
    (nasnet.NASNetMobile, 1056),
    (nasnet.NASNetLarge, 4032),
]

MODEL_LIST = MODEL_LIST_NO_NASNET + NASNET_LIST

MODELS_UNSUPPORTED_CHANNELS_FIRST = ["ConvNeXt", "NASNet", "RegNetX", "RegNetY"]
# Add each data format for each model
test_parameters_with_image_data_format = [
    (
        "{}_{}".format(model[0].__name__, image_data_format),
        *model,
        image_data_format,
    )
    for image_data_format in ["channels_first", "channels_last"]
    for model in MODEL_LIST
]

# Parameters for loading weights for MobileNetV3.
# (class, alpha, minimalistic, include_top)
MOBILENET_V3_FOR_WEIGHTS = [
    (mobilenet_v3.MobileNetV3Large, 0.75, False, False),
    (mobilenet_v3.MobileNetV3Large, 1.0, False, False),
    (mobilenet_v3.MobileNetV3Large, 1.0, True, False),
    (mobilenet_v3.MobileNetV3Large, 0.75, False, True),
    (mobilenet_v3.MobileNetV3Large, 1.0, False, True),
    (mobilenet_v3.MobileNetV3Large, 1.0, True, True),
    (mobilenet_v3.MobileNetV3Small, 0.75, False, False),
    (mobilenet_v3.MobileNetV3Small, 1.0, False, False),
    (mobilenet_v3.MobileNetV3Small, 1.0, True, False),
    (mobilenet_v3.MobileNetV3Small, 0.75, False, True),
    (mobilenet_v3.MobileNetV3Small, 1.0, False, True),
    (mobilenet_v3.MobileNetV3Small, 1.0, True, True),
]


class ApplicationsTest(tf.test.TestCase, parameterized.TestCase):
    def setUp(self):
        self.original_image_data_format = backend.image_data_format()

    def tearDown(self):
        backend.set_image_data_format(self.original_image_data_format)

    @classmethod
    def assertShapeEqual(cls, shape1, shape2):
        if len(shape1) != len(shape2):
            raise AssertionError(
                f"Shapes are different rank: {shape1} vs {shape2}"
            )
        for v1, v2 in zip(shape1, shape2):
            if v1 != v2:
                raise AssertionError(f"Shapes differ: {shape1} vs {shape2}")

    def skip_if_invalid_image_data_format_for_model(
        self, app, image_data_format
    ):
        does_not_support_channels_first = any(
            [
                unsupported_name.lower() in app.__name__.lower()
                for unsupported_name in MODELS_UNSUPPORTED_CHANNELS_FIRST
            ]
        )
        if (
            image_data_format == "channels_first"
            and does_not_support_channels_first
        ):
            self.skipTest(
                "{} does not support channels first".format(app.__name__)
            )

    @parameterized.named_parameters(test_parameters_with_image_data_format)
    def test_application_base(self, app, _, image_data_format):
        self.skip_if_invalid_image_data_format_for_model(app, image_data_format)
        backend.set_image_data_format(image_data_format)
        # Can be instantiated with default arguments
        model = app(weights=None)
        # Can be serialized and deserialized
        config = model.get_config()
        if "ConvNeXt" in app.__name__:
            custom_objects = {"LayerScale": convnext.LayerScale}
            with utils.custom_object_scope(custom_objects):
                reconstructed_model = model.__class__.from_config(config)
        else:
            reconstructed_model = model.__class__.from_config(config)
        self.assertEqual(len(model.weights), len(reconstructed_model.weights))
        backend.clear_session()

    @parameterized.named_parameters(test_parameters_with_image_data_format)
    def test_application_notop(self, app, last_dim, image_data_format):
        self.skip_if_invalid_image_data_format_for_model(app, image_data_format)
        backend.set_image_data_format(image_data_format)
        if image_data_format == "channels_first":
            input_shape = (3, None, None)
            correct_output_shape = (None, last_dim, None, None)
            channels_axis = 1
        else:
            input_shape = (None, None, 3)
            correct_output_shape = (None, None, None, last_dim)
            channels_axis = -1

        if "NASNet" in app.__name__:
            only_check_last_dim = True
        else:
            only_check_last_dim = False
        output_shape = app(
            weights=None, include_top=False, input_shape=input_shape
        ).output_shape
        if only_check_last_dim:
            self.assertEqual(output_shape[channels_axis], last_dim)
        else:
            self.assertShapeEqual(output_shape, correct_output_shape)
        backend.clear_session()

    @parameterized.named_parameters(test_parameters_with_image_data_format)
    def test_application_notop_custom_input_shape(
        self, app, last_dim, image_data_format
    ):
        self.skip_if_invalid_image_data_format_for_model(app, image_data_format)
        backend.set_image_data_format(image_data_format)
        if image_data_format == "channels_first":
            input_shape = (3, 224, 224)
            channels_axis = 1
        else:
            input_shape = (224, 224, 3)
            channels_axis = -1
        output_shape = app(
            weights="imagenet", include_top=False, input_shape=input_shape
        ).output_shape

        self.assertEqual(output_shape[channels_axis], last_dim)

    @parameterized.parameters(MODEL_LIST)
    def test_application_pooling(self, app, last_dim):
        output_shape = app(
            weights=None, include_top=False, pooling="avg"
        ).output_shape
        self.assertShapeEqual(output_shape, (None, last_dim))

    @parameterized.parameters(MODEL_LIST)
    def test_application_classifier_activation(self, app, _):
        if "RegNet" in app.__name__:
            self.skipTest("RegNet models do not support classifier activation")
        model = app(
            weights=None, include_top=True, classifier_activation="softmax"
        )
        last_layer_act = model.layers[-1].activation.__name__
        self.assertEqual(last_layer_act, "softmax")

    @parameterized.named_parameters(test_parameters_with_image_data_format)
    def test_application_variable_input_channels(
        self, app, last_dim, image_data_format
    ):
        self.skip_if_invalid_image_data_format_for_model(app, image_data_format)
        backend.set_image_data_format(image_data_format)
        if backend.image_data_format() == "channels_first":
            input_shape = (1, None, None)
            correct_output_shape = (None, last_dim, None, None)
        else:
            input_shape = (None, None, 1)
            correct_output_shape = (None, None, None, last_dim)
        output_shape = app(
            weights=None, include_top=False, input_shape=input_shape
        ).output_shape

        self.assertShapeEqual(output_shape, correct_output_shape)
        backend.clear_session()

        if backend.image_data_format() == "channels_first":
            input_shape = (4, None, None)
        else:
            input_shape = (None, None, 4)
        output_shape = app(
            weights=None, include_top=False, input_shape=input_shape
        ).output_shape

        self.assertShapeEqual(output_shape, correct_output_shape)
        backend.clear_session()

    @parameterized.parameters(*MOBILENET_V3_FOR_WEIGHTS)
    def test_mobilenet_v3_load_weights(
        self, mobilenet_class, alpha, minimalistic, include_top
    ):
        mobilenet_class(
            input_shape=(224, 224, 3),
            weights="imagenet",
            alpha=alpha,
            minimalistic=minimalistic,
            include_top=include_top,
        )

    @parameterized.named_parameters(test_parameters_with_image_data_format)
    @test_utils.run_v2_only
    def test_model_checkpoint(self, app, _, image_data_format):
        self.skip_if_invalid_image_data_format_for_model(app, image_data_format)
        backend.set_image_data_format(image_data_format)

        model = app(weights=None)

        checkpoint = tf.train.Checkpoint(model=model)
        checkpoint_manager = tf.train.CheckpointManager(
            checkpoint,
            directory=os.path.join(self.get_temp_dir(), model.name),
            max_to_keep=1,
        )
        checkpoint_manager.save(checkpoint_number=1)


if __name__ == "__main__":
    tf.test.main()
