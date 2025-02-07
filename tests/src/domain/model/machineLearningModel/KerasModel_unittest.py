import unittest

import numpy as np
import pandas as pd

from src.adv_xai_fulfilment.domain.model.machineLearningModel.keras_model import (
    KerasModel,
)
from src.adv_xai_fulfilment.domain.model.explainers.responseData.feature_description import (
    FeatureDescription,
)


class SilentKerasModel(KerasModel):
    def load(self, path: str) -> "KerasModel":
        return self


class TestKerasModel(unittest.TestCase):
    def test_supported_frameworks(self):
        result = KerasModel.supported_frameworks()
        self.assertIsInstance(result, list)
        self.assertTrue("keras" in result)
        self.assertTrue("tensorflow" in result)
        self.assertTrue("tensorflow-keras" in result)

    def test_get_feature_importance(self):
        model = SilentKerasModel("filename")
        feature_names = [
            FeatureDescription(
                type="text",
                name="Feature1",
                source="source1",
                description="description1",
            ),
            FeatureDescription(
                type="text",
                name="Feature2",
                source="source2",
                description="description2",
            ),
        ]
        shap_values = np.array([[0.1, 0.3], [0.2, 0.4], [-0.1, -0.2]])
        result = model.get_feature_importance(feature_names, shap_values)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue("[Feature1, Feature2]" in str(result["Feature"]))
        self.assertTrue("[0.13333333333333333, 0.3]" in str(result["Importance"]))
