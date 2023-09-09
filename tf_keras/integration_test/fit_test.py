"""Test Model.fit across a diverse range of models."""

import tensorflow.compat.v2 as tf
from absl.testing import parameterized

from tf_keras.integration_test.models import bert
from tf_keras.integration_test.models import dcgan
from tf_keras.integration_test.models import edge_case_model
from tf_keras.integration_test.models import efficientnet_v2
from tf_keras.integration_test.models import input_spec
from tf_keras.integration_test.models import low_level_model
from tf_keras.integration_test.models import mini_unet
from tf_keras.integration_test.models import mini_xception
from tf_keras.integration_test.models import retinanet
from tf_keras.integration_test.models import structured_data_classification
from tf_keras.integration_test.models import text_classification
from tf_keras.integration_test.models import timeseries_forecasting
from tf_keras.integration_test.models import vae
from tf_keras.testing_infra import test_combinations
from tf_keras.testing_infra import test_utils

# from tf_keras.integration_test.models import ctc_speech_rnn
# from tf_keras.integration_test.models import translation


def get_dataset(data_specs, batch_size):
    values = tf.nest.map_structure(input_spec.spec_to_value, data_specs)
    dataset = (
        tf.data.Dataset.from_tensor_slices(values)
        .prefetch(batch_size * 2)
        .batch(batch_size)
    )
    return dataset


@test_utils.run_v2_only
class FitTest(test_combinations.TestCase):
    @parameterized.named_parameters(
        ("bert", bert),
        # ("ctc_speech_rnn", ctc_speech_rnn),  # Buggy?
        ("dcgan", dcgan),
        ("edge_case_model", edge_case_model),
        ("efficientnet_v2", efficientnet_v2),
        ("low_level_model", low_level_model),
        ("mini_unet", mini_unet),
        ("mini_xception", mini_xception),
        ("retinanet", retinanet),
        ("structured_data_classification", structured_data_classification),
        ("text_classification", text_classification),
        ("timeseries_forecasting", timeseries_forecasting),
        # ("translation", translation),  # Buggy?
        ("vae", vae),
    )
    def test_fit_on_all_models_with_sync_preprocessing(self, module):
        batch_size = 4
        data_specs = module.get_data_spec(batch_size * 3)
        dataset = get_dataset(data_specs, batch_size)

        model = module.get_model(
            build=True,
            compile=True,
            jit_compile=False,
            include_preprocessing=True,
        )
        model.fit(dataset, epochs=1)

    @parameterized.named_parameters(
        ("bert", bert),
        # ("ctc_speech_rnn", ctc_speech_rnn),  # Buggy?
        ("dcgan", dcgan),
        ("edge_case_model", edge_case_model),
        ("efficientnet_v2", efficientnet_v2),
        ("low_level_model", low_level_model),
        # ("mini_unet", mini_unet),  # Not XLA compatible b/c of UpSampling2D
        ("mini_xception", mini_xception),
        # ("retinanet", retinanet),  # Not XLA compatible b/c of UpSampling2D
        ("structured_data_classification", structured_data_classification),
        ("text_classification", text_classification),
        ("timeseries_forecasting", timeseries_forecasting),
        # ("translation", translation),  # Buggy?
        ("vae", vae),
    )
    def test_fit_on_all_models_with_async_preprocessing_and_xla(self, module):
        batch_size = 4
        data_specs = module.get_data_spec(batch_size * 3)
        dataset = get_dataset(data_specs, batch_size)
        preprocessor = module.get_input_preprocessor()
        if preprocessor is not None:
            dataset = dataset.map(lambda x, y: (preprocessor(x), y))

        model = module.get_model(
            build=True,
            compile=True,
            jit_compile=True,
            include_preprocessing=False,
        )
        model.fit(dataset, epochs=1)


if __name__ == "__main__":
    tf.test.main()
