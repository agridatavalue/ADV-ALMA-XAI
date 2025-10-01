import unittest

import numpy as np
import pandas as pd
from shap import KernelExplainer

from src.adv_xai_fulfilment.domain.model.model_data import ModelData
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers import KernelExplainerExplainer
from src.adv_xai_fulfilment.domain.model.machine_learning_model.keras_model import KerasModel


class SilentKerasModel(KerasModel):
    def load(self, data: dict) -> KerasModel:
        self.handler = type("MockHandler", (object,), {"predict": lambda self, x: x})
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
                subject_name="subject_name",
                model_category="Regression",
                feature_names=[],
                feature_descriptions=[],
            )
        )
        
        model_data = ModelData()
        model_data.x_predict = pd.DataFrame(np.array([[0, 0], [1, 1]]))
        
        self.testObj.build(
            SilentKerasModel(filename="test", layers=[]),
            model_data
        )
        self.assertIsInstance(self.testObj.build_result, KernelExplainer)
