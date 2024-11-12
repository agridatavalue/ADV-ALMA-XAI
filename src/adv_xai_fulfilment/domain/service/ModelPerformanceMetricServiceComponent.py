import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from ..model.Model import Model
from src.adv_xai_fulfilment.infrastructure.Constants import Errors


class ModelPerformanceMetricServiceComponent:

    def get_data(self, model: Model, data: dict) -> dict:
        assert isinstance(data, dict), Errors.DATA_NOT_DICT

        y_pred = [y[0] for y in model.handler.predict(data.get("x"))]
        return {"y_pred": y_pred, "y_true": data.get("y")}

    def get_metrics(self, prediction_target: int, model: Model, data: dict) -> dict:
        if not data or not model:
            return {}

        y_pred = [y[prediction_target] for y in model.handler.predict(data.get("x"))]

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
