import numpy as np
import pandas as pd

from .explainer_response_data import ExplainerResponseData

class Targets(ExplainerResponseData):
    _x_real: pd.Series
    _y_real: pd.DataFrame
    _y_predicted: np.array

    def __init__(self):
        super().__init__(endpoint='targets')
        self._x_real = None
        self._y_real = None
        self._y_predicted = None

    def set_x(self, real) -> 'Targets':
        self._x_real = real
        return self

    def set_y(self, real, predicted) -> 'Targets':
        self._y_real = real
        self._y_predicted = predicted
        return self
    
    def _safe_to_list(self, obj):
        if obj is None:
            return None
        if isinstance(obj, list):
            return obj
        if hasattr(obj, "values"):
            return obj.values.tolist()
        return obj.tolist()

    def to_dict(self) -> dict:
        y_real = self._safe_to_list(self._y_real)
        if y_real is not None and all(isinstance(y, (list, tuple)) for y in y_real):
            y_real = sum(y_real, [])

        return {
            'y_real': y_real,
            'x_real': self._safe_to_list(self._x_real),
            'y_predicted': self._safe_to_list(self._y_predicted)
        }