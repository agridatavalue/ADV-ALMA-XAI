import os
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


class TestModelTranslator(unittest.TestCase):
    def test_translate(self):
        testObj = ModelTranslator()

        with open("model.h5", "w") as f:
            f.write("")

        self.assertIsInstance(
            testObj.with_("keras").and_("cnn").translate("model.h5"),
            KerasModel,
        )
        self.assertIsInstance(
            testObj.with_("torch").and_("cnn").translate("model.h5"),
            TorchModel,
        )
        self.assertIsInstance(
            testObj.with_("scikit-learn").and_("cnn").translate("model.h5"),
            ScikitLearnModel,
        )

        os.remove("model.h5")
