from typing import Union
import numpy as np
from sklearn.metrics import roc_auc_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.metrics import accuracy_score, precision_score, average_precision_score

from ..model.model import Model
from ..model.data_type import DataType
from ..model.model_data import ModelData
from ..model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from ..model.explainers.response_data import ModelPerformance, ModelPerformanceMetrics


class ModelPerformanceServiceComponent:

    def get_data(
        self, model: Model, data: ModelData, prediction_target_index: int = 0
    ) -> ModelPerformance:
        assert isinstance(data, ModelData), Errors.MODEL_DATA_NOT_MODEL_DATA_TYPE

        y_true = data.get_y_for_prediction_target(prediction_target_index).to_list()
        predictions = model.handler.predict(data.x)
        if predictions.ndim == 1:  # 1D array
            y_pred = [float(y) for y in predictions]
        else:  # 2D array
            y_pred = [float(y[prediction_target_index]) for y in predictions]

        return ModelPerformance(y_true=y_true, y_pred=y_pred)

    def get_metrics(
        self,
        *,
        model: Model,
        data: Union[ModelData, list[ModelData]],
        prediction_target: str,
        model_metadata: ModelMetaData,
    ) -> ModelPerformanceMetrics:
        assert isinstance(model, Model), Errors.MODEL_NOT_MODEL

        if model_metadata.data_type == DataType.TABULAR:
            if data.is_empty or not model:
                return ModelPerformanceMetrics()

            if data.y.empty:
                return ModelPerformanceMetrics()
        elif model_metadata.data_type == DataType.IMAGE:
            if not data:
                return ModelPerformanceMetrics()

        prediction_target_index = model_metadata.index_of_target_name(prediction_target)

        if model_metadata.is_regression:
            return self.__get_metrics_for_regression(
                prediction_target_index, model, data
            )

        return self.__get_metrics_for_classification(
            prediction_target_index, model, data
        )

    def __get_metrics_for_regression(
        self, prediction_target_index: int, model: Model, data: ModelData
    ) -> ModelPerformanceMetrics:
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

    def __get_metrics_for_classification(
        self, prediction_target_index: int, model: Model, data: ModelData
    ) -> ModelPerformanceMetrics:
        y_pred = model.handler.predict(data.x)

        return (
            ModelPerformanceMetrics()
            .add_metric("roc_auc", roc_auc_score(data.y, y_pred))
            .add_metric("accuracy", accuracy_score(data.y, y_pred))
            .add_metric("f1", f1_score(data.y, y_pred, average="weighted"))
            .add_metric("recall", recall_score(data.y, y_pred, average="weighted"))
            .add_metric(
                "precision", precision_score(data.y, y_pred, average="weighted")
            )
            .add_metric(
                "pr_auc", average_precision_score(data.y, y_pred, average="weighted")
            )
        )
