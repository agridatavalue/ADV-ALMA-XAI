import unittest

from alibi.explainers import ALE

from src.adv_xai_fulfilment.domain.model.explainers import AleExplainer
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.machine_learning_model import KerasModel


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
                feature_names=[],
                subject_name="subject_name",
                model_category="Regression",
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
