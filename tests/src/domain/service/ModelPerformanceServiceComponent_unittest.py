import unittest
from unittest.mock import MagicMock

import pandas as pd

from src.adv_xai_fulfilment.domain.model.ModelData import ModelData
from src.adv_xai_fulfilment.domain.model.machineLearningModel.KerasModel import (
    KerasModel,
)
from src.adv_xai_fulfilment.domain.service.ModelPerformanceServiceComponent import (
    ModelPerformanceServiceComponent,
)


class SilentKerasModel(KerasModel):
    def load(self, model_path) -> "SilentKerasModel":
        self.handler = MagicMock()
        self.handler.predict = MagicMock(side_effect=lambda x: [[0]] * len(x))
        return self


class TestModelPerformanceServiceComponent(unittest.TestCase):
    def test_get_data(self):
        testObj = ModelPerformanceServiceComponent()

        model_data = ModelData()
        model_data.x = pd.DataFrame({"target": [1, 2, 3]})
        model_data.y = pd.DataFrame({"target": [1, 2, 3]})

        self.assertEqual(
            testObj.get_data(
                data=model_data,
                model=SilentKerasModel(filename="test"),
                prediction_target_index=0,
            ),
            {"y_pred": [0.0, 0.0, 0.0], "y_true": [1, 2, 3]},
        )

    def test_get_metrics(self):
        testObj = ModelPerformanceServiceComponent()

        model_data = ModelData()
        model_data.x = pd.DataFrame({"target": [1, 2, 3]})
        model_data.y = pd.DataFrame({"target": [1, 2, 3]})

        actual = testObj.get_metrics(
            data=model_data,
            prediction_target_index=0,
            model=SilentKerasModel(filename="test"),
        )

        self.assertIsInstance(actual, dict)
        self.assertTrue("Mean Squared Error (MSE)" in actual)
        self.assertTrue("R-Squared (R²)" in actual)
        self.assertTrue("Mean Absolute Error (MAE)" in actual)
        self.assertTrue("Root Mean Squared Error (RMSE)" in actual)
        self.assertTrue("Mean Absolute Percentage Error (MAPE)" in actual)
