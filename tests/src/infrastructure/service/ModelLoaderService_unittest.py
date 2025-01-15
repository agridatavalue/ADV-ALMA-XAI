import unittest
from unittest.mock import MagicMock, patch

from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.Model import Model
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.domain.model.machineLearningModel.KerasModel import (
    KerasModel,
)
from src.adv_xai_fulfilment.infrastructure.service.ModelLoaderService import (
    ModelLoaderService,
)


class SilentKerasModel(KerasModel):
    def load(self, path: str) -> "SilentKerasModel":
        self.handler = MagicMock()
        return self


class ModelLoaderServiceTest(unittest.TestCase):
    testObj: ModelLoaderService

    def test_upload_explainer(self):
        testObj = ModelLoaderService()
        testObj._bucketRepository = MagicMock()
        testObj._bucketRepository.upload_to = MagicMock(return_value="test")

        explainer = MagicMock()
        explainer.file_name = "test.pkl"
        explainer.build_result = "test"

        actual = testObj.upload_explainer(
            explainer,
            ExplainerIdentifier(
                model="test",
                pilot=Pilot("test"),
                metadata=ModelMetaData("", "", "", "", "", ""),
                prediction_target="test",
            ),
        )

        self.assertEqual(actual, "test")

    @patch("os.getenv", return_value="/mock/temp")
    def test_load_from(self, mock_getenv):
        testObj = ModelLoaderService()
        testObj._bucketRepository.download_from = MagicMock(return_value="test.json")
        testObj._model_translator.translate = MagicMock(
            return_value=SilentKerasModel(filename="test")
        )

        with open("test.json", "w") as f:
            f.write('{"framework": "test", "algorithm": "test"}')

        actual = testObj.load_from("test.json", MagicMock())

        self.assertIsInstance(actual, Model)
