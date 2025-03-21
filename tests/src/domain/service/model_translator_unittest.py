import unittest

from src.adv_xai_fulfilment.domain.service import ModelTranslator
from src.adv_xai_fulfilment.domain.model.machine_learning_model.keras_model import KerasModel
from src.adv_xai_fulfilment.domain.model.machine_learning_model.torch_model import TorchModel
from src.adv_xai_fulfilment.domain.model.machine_learning_model.scikitlearn_model import ScikitLearnModel


class SilentKerasModel(KerasModel):
    def load(self, path: str) -> "KerasModel":
        return self


class SilentTorchModel(TorchModel):
    def load(self, path: str) -> "TorchModel":
        return self


class SilentScikitLearnModel(ScikitLearnModel):
    def load(self, path: str) -> "ScikitLearnModel":
        return self


class TestModelTranslator(unittest.TestCase):
    def test_translate(self):
        testObj = ModelTranslator(
            models=[
                SilentKerasModel,
                SilentTorchModel,
                SilentScikitLearnModel,
            ]
        )

        self.assertIsInstance(
            testObj.with_("keras").and_("cnn").translate("model.h5"),
            SilentKerasModel,
        )
        self.assertIsInstance(
            testObj.with_("torch").and_("cnn").translate("model.h5"),
            SilentTorchModel,
        )
        self.assertIsInstance(
            testObj.with_("scikit-learn").and_("cnn").translate("model.h5"),
            SilentScikitLearnModel,
        )
