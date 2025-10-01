import unittest
from unittest.mock import MagicMock

import numpy as np
import pandas as pd

from src.adv_xai_fulfilment.domain.model.model_data import ModelData
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.machine_learning_model.keras_model import KerasModel
from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    ModelPerformance,
    ModelPerformanceMetrics,
)
from src.adv_xai_fulfilment.domain.service.model_performance_service_component import (
    ModelPerformanceServiceComponent,
)


class SilentKerasModel(KerasModel):
    def load(self, model_path) -> "SilentKerasModel":
        self.handler = MagicMock()
        self.handler.predict = MagicMock(
            return_value=np.array([[2.0, 0], [4.0, 0], [6.0, 0]])
        )
        return self


class TestModelPerformanceServiceComponent(unittest.TestCase):
    def test_get_data(self):
        testObj = ModelPerformanceServiceComponent()

        model_data = ModelData()
        model_data.x_predict = pd.DataFrame({"target": [1, 2, 3]})
        model_data.y_predict = np.ndarray([2, 4, 6])
        model_data.data_train = pd.DataFrame({"target": [1, 2, 3]})

        actual = testObj.get_data(
            data=model_data,
            prediction_target="target",
        )
        self.assertIsInstance(actual, ModelPerformance)
        self.assertEqual(actual.y_pred, [2.0, 4.0, 6.0])
        self.assertEqual(actual.y_true, [1, 2, 3])

    def test_get_metrics(self):
        testObj = ModelPerformanceServiceComponent()

        model_data = ModelData()
        model_data.x_train = pd.DataFrame({"target": [1, 2, 3]})
        model_data.y_train = pd.DataFrame({"target": [1, 2, 3]})
        model_data.x_predict = pd.DataFrame({"target": [1, 2, 3]})
        model_data.y_predict = np.ndarray([2, 4, 6])
        model_data.data_train = pd.DataFrame({"target": [1, 2, 3]})

        model_metadata = MagicMock(spec=ModelMetaData)
        model_metadata.is_regression = True
        model_metadata.feature_names = ["target"]

        actual = testObj.get_metrics(
            data=model_data,
            model_metadata=model_metadata,
            model=SilentKerasModel(filename="test", layers=[]),
        )

        self.assertIsInstance(actual, ModelPerformanceMetrics)
        self.assertTrue("Mean Squared Error (MSE)" in actual.metrics)
        self.assertTrue("R-Squared (R²)" in actual.metrics)
        self.assertTrue("Mean Absolute Error (MAE)" in actual.metrics)
        self.assertTrue("Root Mean Squared Error (RMSE)" in actual.metrics)
        self.assertTrue("Mean Absolute Percentage Error (MAPE)" in actual.metrics)
