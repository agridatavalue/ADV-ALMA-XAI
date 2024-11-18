import unittest

from src.adv_xai_fulfilment.domain.service.ModelTranslator import ModelTranslator
from src.adv_xai_fulfilment.domain.model.machineLearningModel.TorchModel import (
    TorchModel,
)
from src.adv_xai_fulfilment.domain.model.machineLearningModel.KerasModel import (
    KerasModel,
)
from src.adv_xai_fulfilment.domain.model.machineLearningModel.ScikitLearnModel import (
    ScikitLearnModel,
)


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
