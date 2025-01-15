import os
import unittest
from os import path
from dotenv import load_dotenv

from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.explainers.AleExplainer import AleExplainer
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)

load_dotenv()


class TestDataLoaderService(unittest.TestCase):
    def setUp(self):
        self.testObj = DataLoaderService()

    def test_load_explainer_metadata(self):
        metadata_filepath: str = path.join(
            os.getenv("temp"), "test_load_explainer_metadata.json"
        )
        with open(metadata_filepath, "w") as f:
            f.write(
                '{"possible_explainers": [{"name": "AleExplainer"}], "target_name": "test", "meta_data": {"data_type": "test", "algorithm": "test", "framework": "test", "model_type": "test", "subject_name": "test", "target_names": [], "model_category": "test", "feature_descriptions": {}}, "metrics": {}}'
            )

        self.testObj._bucketRepository.download_from = (
            lambda bucket_name, object_name: metadata_filepath
        )
        self.testObj._explainer_metadata_translator.translate = (
            lambda explainer_metadata: ExplainerMetaData(
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
            )
        )

        actual = self.testObj.load_explainer_metadata(
            ExplainerIdentifier(
                model="test",
                metadata="test",
                prediction_target="test",
                pilot=Pilot("test"),
            )
        )

        self.assertIsInstance(actual, ExplainerMetaData)

    def test_upload(self):
        self.testObj._bucketRepository.upload_to = (
            lambda bucket_name, target_filepath, local_filepath: "test/metadata.json"
        )
        dest = self.testObj.upload(
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
