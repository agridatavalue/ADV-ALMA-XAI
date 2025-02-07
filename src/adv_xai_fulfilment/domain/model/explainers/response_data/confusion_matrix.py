import numpy as np
import pandas as pd

from .explainer_response_data import ExplainerResponseData


class ConfusionMatrix(ExplainerResponseData):
    _data: pd.DataFrame

    def __init__(self):
        super().__init__("confusion-matrix")
        self._data = pd.DataFrame()

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @data.setter
    def data(self, data: pd.DataFrame):
        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data)

        assert isinstance(data, pd.DataFrame), "data must be a pandas DataFrame"
        self._data = data

    def to_dict(self) -> dict:
        data_dict = self.data.to_dict()
        if 0 in data_dict:
            data_dict["actual"] = data_dict.pop(0)
        if 1 in data_dict:
            data_dict["predicted"] = data_dict.pop(1)
        return data_dict
