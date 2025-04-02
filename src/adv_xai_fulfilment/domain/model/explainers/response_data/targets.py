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
    
    def to_dict(self) -> dict:
        y_real = self._y_real.values.tolist()
        if all(isinstance(y, list) or isinstance(y, tuple) for y in y_real):
            y_real = sum(self._y_real.values.tolist(), [])

        return {
            'y_real': y_real,
            'x_real': self._x_real.tolist(),
            'y_predicted': self._y_predicted.tolist(),
        }