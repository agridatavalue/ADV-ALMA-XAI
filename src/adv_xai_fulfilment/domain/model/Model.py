from __future__ import annotations
import numpy as np
import pandas as pd


class Model:
    name: str
    handler: any
    filename: str

    def __init__(self, handler: any, name: str = "", filename: str = ""):
        self.name = name
        self.handler = handler
        self.filename = filename

    @staticmethod
    def supported_frameworks() -> list[str]: ...

    def get_feature_importance(
        self, feature_names: list, shap_values: np.array
    ) -> pd.DataFrame: ...
