import os
import unittest
from unittest.mock import MagicMock, patch

from src.adv_xai_fulfilment.domain.model.model import Model
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.domain.model.machine_learning_model.keras_model import KerasModel
from src.adv_xai_fulfilment.infrastructure.service.ModelLoaderService import ModelLoaderService


class SilentKerasModel(KerasModel):
    def load(self, path: str) -> "SilentKerasModel":
        self.handler = MagicMock()
        return self


class ModelLoaderServiceTest(unittest.TestCase):
    testObj: ModelLoaderService

    @patch("os.getenv", return_value="/mock/temp")
    def test_load_from(self, mock_getenv):
        testObj = ModelLoaderService(bucketRepository=MagicMock())
        testObj._bucketRepository.download_from = MagicMock(return_value="test.json")
        testObj._model_translator.translate = MagicMock(
            return_value=SilentKerasModel(filename="test")
        )

        with open("test.json", "w") as f:
            f.write('{"framework": "test", "algorithm": "test"}')

        actual = testObj.load_from(
            ExplainerIdentifier(
                model='test.json', partner='test', metadata_identifier='test', prediction_target='test'
            ), 
            ModelMetaData(
                data_type="test", framework="test", algorithm="test", 
                model_type="test", subject_name="test", model_category="REGRESSION"
            )
        )

        os.remove("test.json")

        self.assertIsInstance(actual, Model)
