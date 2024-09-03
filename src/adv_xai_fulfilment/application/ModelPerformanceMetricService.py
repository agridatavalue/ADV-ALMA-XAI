import os
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from ..domain.model.Model import Model
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService


class ModelPerformanceMetricService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()

    def get_data(self, model_filename: str) -> dict:
        selected_model: Model = self._model_loader_service.load_from(model_filename)

        data: dict = self._data_loader_service.load_data(
            bucket_name=os.getenv("DATA_FOLDER_PATH"), file_path="crop"
        )

        y_pred = [y[0] for y in selected_model.handler.predict(data.get("x"))]
        return {"y_pred": y_pred, "y_true": data.get("y")}

    def get_metrics(self, model_filename: str) -> dict:
        selected_model: Model = self._model_loader_service.load_from(model_filename)

        data: dict = self._data_loader_service.load_data(
            bucket_name=os.getenv("DATA_FOLDER_PATH"), file_path="crop"
        )

        y_pred = [y[0] for y in selected_model.handler.predict(data.get("x"))]

        mse = mean_squared_error(data.get("y"), y_pred)
        mae = mean_absolute_error(data.get("y"), y_pred)

        return {
            "Mean Squared Error (MSE)": mse,
            "R-Squared (R²)": r2_score(data.get("y"), y_pred),
            "Mean Absolute Error (MAE)": mae,
            "Root Mean Squared Error (RMSE)": np.sqrt(mse),
            "Mean Absolute Percentage Error (MAPE)": (
                (mae / data.get("y")).mean()
            ).to_list()[0],
        }
