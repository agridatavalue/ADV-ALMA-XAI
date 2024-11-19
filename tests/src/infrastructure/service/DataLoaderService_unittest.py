import unittest

from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.explainers.AleExplainer import AleExplainer
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)


class TestDataLoaderService(unittest.TestCase):

    def test_upload(self):
        testObj = DataLoaderService()
        testObj._bucketRepository.upload_to = (
            lambda bucket_name, target_filepath, local_filepath: "test/metadata.json"
        )
        dest = testObj.upload(
            target="test",
            model_category="test",
            model_filename="test",
            explainer_data=ExplainerMetaData(
                possible_explainers=[AleExplainer()],
                target_name="test",
                meta_data=ModelMetaData(
                    data_type="test",
                    algorithm="test",
                    framework="test",
                    model_type="test",
                    subject_name="test",
                    target_names=[],
                    model_category="test",
                    feature_descriptions=[],
                ),
                metrics={},
            ),
        )

        self.assertEqual(dest, "test/metadata.json")
