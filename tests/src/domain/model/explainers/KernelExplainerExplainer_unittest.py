import unittest
from shap import KernelExplainer
import numpy as np

from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.machineLearningModel.KerasModel import (
    KerasModel,
)
from src.adv_xai_fulfilment.domain.model.explainers.KernelExplainerExplainer import (
    KernelExplainerExplainer,
)


class SilentKerasModel(KerasModel):
    def load(self, path: str) -> KerasModel:
        return self


class TestKernelExplainerExplainer(unittest.TestCase):
    def setUp(self):
        self.testObj = KernelExplainerExplainer()

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
                handler=type(
                    "MockHandler", (object,), {"predict": lambda self: np.array([0])}
                ),
            ),
            {"x": np.array([[0]])},
        )
        self.assertIsInstance(self.testObj.build_result, KernelExplainer)
