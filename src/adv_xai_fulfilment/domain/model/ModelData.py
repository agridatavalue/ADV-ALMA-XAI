import pandas as pd


class ModelData:
    _x: pd.DataFrame
    _y: pd.DataFrame

    def __init__(self):
        self._x = None
        self._y = None

    @property
    def x(self) -> pd.DataFrame:
        return self._x

    @x.setter
    def x(self, x: pd.DataFrame):
        self._x = x

    @property
    def y(self) -> pd.DataFrame:
        return self._y

    @y.setter
    def y(self, y: pd.DataFrame):
        self._y = y

    def get_y_for_prediction_target(self, target: str) -> pd.DataFrame:
        return self._y.iloc[:, target]

    @property
    def is_empty(self) -> bool:
        return self._x is None or self._y is None
