import unittest
from alibi.explainers import ALE

from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.AleExplainer import AleExplainer
from src.adv_xai_fulfilment.domain.model.machineLearningModel.KerasModel import (
    KerasModel,
)


class SilentKerasModel(KerasModel):
    def load(self, path: str) -> KerasModel:
        return self


class TestAleExplainer(unittest.TestCase):
    def setUp(self):
        self.testObj = AleExplainer()

    def test_build(self):
        self.testObj.meta_data = None
        with self.assertRaises(Exception):
            self.testObj.build(None, None)

        self.testObj.set_meta_data(
            ModelMetaData(
                data_type="Text",
                algorithm="algorithm",
                framework="framework",
                model_type="BlackBox",
                target_names=[],
                model_category="Regression",
                feature_names=[],
                feature_descriptions=[],
            )
        )
        self.testObj.build(
            SilentKerasModel(
                filename="test",
                handler=type("MockHandler", (object,), {"predict": lambda self, x: x}),
            ),
            None,
        )
        self.assertIsInstance(self.testObj.build_result, ALE)
