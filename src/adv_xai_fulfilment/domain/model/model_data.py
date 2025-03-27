import pandas as pd


class ModelData:
    _x: pd.DataFrame
    _y: pd.DataFrame
    _image_path: str

    def __init__(self):
        self._x = None
        self._y = None
        self._image_path = ''

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

    @property
    def image_path(self) -> str:
        return self._image_path

    @image_path.setter
    def image_path(self, image: str):
        assert isinstance(image, str)
        self._image_path = image

    def get_y_for_prediction_target(self, target: str) -> pd.DataFrame:
        return self._y.iloc[:, target]

    @property
    def is_empty(self) -> bool:
        return self._x is None or self._y is None

    def __repr__(self) -> str:
        return f"ModelData(x={self._x}, y={self._y}, image_path={self._image_path})"
