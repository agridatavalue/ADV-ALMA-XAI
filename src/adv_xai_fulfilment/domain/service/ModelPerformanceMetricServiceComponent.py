import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from ..model.Model import Model
from src.adv_xai_fulfilment.infrastructure.Constants import Errors


class ModelPerformanceMetricServiceComponent:

    def get_data(self, model: Model, data: dict) -> dict:
        assert isinstance(data, dict), Errors.DATA_NOT_DICT

        y_pred = [y[0] for y in model.handler.predict(data.get("x"))]
        return {"y_pred": y_pred, "y_true": data.get("y")}

    def get_metrics(
        self,
        prediction_target_index: int,
        model: Model,
        data: dict["x" : pd.DataFrame, "y" : pd.DataFrame],
    ) -> dict:
        if not data or not model:
            return {}

        y_pred = [
            y[prediction_target_index] for y in model.handler.predict(data.get("x"))
        ]
        y_true = data.get("y").iloc[:, 0]

        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)

        return {
            "Mean Squared Error (MSE)": mse,
            "R-Squared (R²)": r2_score(y_true, y_pred),
            "Mean Absolute Error (MAE)": mae,
            "Root Mean Squared Error (RMSE)": np.sqrt(mse),
            "Mean Absolute Percentage Error (MAPE)": (mae / y_true).mean(),
        }
