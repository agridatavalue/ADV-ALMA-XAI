import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from ..model.Model import Model
from ..model.ModelData import ModelData
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from ..model.explainers.responseData.ModelPerformance import ModelPerformance
from ..model.explainers.responseData.ModelPerformanceMetrics import (
    ModelPerformanceMetrics,
)


class ModelPerformanceServiceComponent:

    def get_data(
        self, model: Model, data: ModelData, prediction_target_index: int = 0
    ) -> ModelPerformance:
        assert isinstance(data, ModelData), Errors.MODEL_DATA_NOT_MODEL_DATA_TYPE

        return ModelPerformance(
            y_true=data.get_y_for_prediction_target(prediction_target_index).to_list(),
            y_pred=[
                float(y[prediction_target_index]) for y in model.handler.predict(data.x)
            ],
        )

    def get_metrics(
        self, prediction_target_index: int, model: Model, data: ModelData
    ) -> ModelPerformanceMetrics:
        if data.is_empty or not model:
            return ModelPerformanceMetrics()

        if data.y.empty:
            return ModelPerformanceMetrics()

        y_pred = None
        predictions = model.handler.predict(data.x)
        if isinstance(predictions, np.ndarray):
            if len(predictions.shape) == 2:  # 2D array
                y_pred = [y[prediction_target_index] for y in predictions]
            elif len(predictions.shape) == 1:  # 1D array
                y_pred = predictions
        y_true = data.y.iloc[:, 0]

        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)

        return (
            ModelPerformanceMetrics()
            .add_metric("Mean Squared Error (MSE)", mse)
            .add_metric("R-Squared (R²)", r2_score(y_true, y_pred))
            .add_metric("Mean Absolute Error (MAE)", mae)
            .add_metric("Root Mean Squared Error (RMSE)", np.sqrt(mse))
            .add_metric("Mean Absolute Percentage Error (MAPE)", (mae / y_true).mean())
        )
