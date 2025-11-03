from typing import Union

import numpy as np
import pandas as pd
from logger import get_logger
from sklearn.metrics import roc_auc_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.metrics import accuracy_score, precision_score, average_precision_score

from ..model.model import Model
from ..model.model_data import ModelData
from ..model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.infrastructure.constants import Errors
from ..model.explainers.response_data import ModelPerformance, ModelPerformanceMetrics

logger = get_logger()


class ModelPerformanceServiceComponent:

    def get_data(self, data: ModelData, prediction_target: str) -> ModelPerformance:
        if not isinstance(data, ModelData):
            raise ValueError(Errors.MODEL_DATA_NOT_MODEL_DATA_TYPE)

        return ModelPerformance(
            y_pred = data.y_predict.tolist() if isinstance(data.y_predict, np.ndarray) else data.y_predict,
            target = prediction_target,
            y_true = (
                data.y_test.to_list() 
                if isinstance(data.y_test, pd.Series) 
                else data.y_test.values.tolist() if isinstance(data.y_test, pd.DataFrame) else data.y_test
            ),
        )

    def get_metrics(
        self,
        *,
        model: Model,
        data: Union[ModelData, list[ModelData]],
        model_metadata: ModelMetaData,
    ) -> ModelPerformanceMetrics:
        if not isinstance(model_metadata, ModelMetaData):
            raise ValueError(Errors.MODEL_NOT_MODEL)
        
        if not model:
            logger.warning("No model provided")
            return ModelPerformanceMetrics()

        if data.is_empty if isinstance(data, ModelData) else all(d.is_empty for d in data):
            logger.warning("No data provided")
            return ModelPerformanceMetrics()

        if model_metadata.is_regression:
            logger.debug("Calculating regression metrics")
            return self.__get_metrics_for_regression(data)

        if model_metadata.is_ts_anomaly_detection:
            logger.debug("Calculating anomaly detection metrics")
            return self.__get_metrics_for_anomaly_detection(data, model_metadata)
        
        logger.debug("Calculating classification metrics")
        return self.__get_metrics_for_classification(data)

    def __get_metrics_for_regression(self, data: ModelData) -> ModelPerformanceMetrics:
        if (data.y_test.empty and data.y_predict):
            return ModelPerformanceMetrics()
        
        mse = mean_squared_error(data.y_test, data.y_predict)
        mae = mean_absolute_error(data.y_test, data.y_predict)
        
        return (ModelPerformanceMetrics()
            .add_metric("Mean Squared Error (MSE)", mse)
            .add_metric("Mean Absolute Error (MAE)", mae)
            .add_metric("Root Mean Squared Error (RMSE)", np.sqrt(mse))
            .add_metric("R-Squared (R²)", r2_score(data.y_test, data.y_predict))
            .add_metric("Mean Absolute Percentage Error (MAPE)", (mae / data.y_test).mean())
        )
            

    def __get_metrics_for_classification(self, data: ModelData) -> ModelPerformanceMetrics:
        return (
            ModelPerformanceMetrics()
            .add_metric("roc_auc", roc_auc_score(data.y_test, data.y_predict))
            .add_metric("accuracy", accuracy_score(data.y_test, data.y_predict))
            .add_metric("f1", f1_score(data.y_test, data.y_predict, average="weighted"))
            .add_metric("recall", recall_score(data.y_test, data.y_predict, average="weighted"))
            .add_metric(
                "precision", precision_score(data.y_test, data.y_predict, average="weighted")
            )
            .add_metric(
                "pr_auc", average_precision_score(data.y_test, data.y_predict, average="weighted")
            )
        )

    def __get_metrics_for_anomaly_detection(
        self, data: ModelData, model_metadata: ModelMetaData
    ) -> ModelPerformanceMetrics:
        if len(model_metadata.target_names) == 0:
            logger.warning("No target names provided in model metadata")
            return ModelPerformanceMetrics()
        
        return self.__get_metrics_for_classification(data)
        