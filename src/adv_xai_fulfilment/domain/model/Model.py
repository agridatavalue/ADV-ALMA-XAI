import os
import numpy as np
import pandas as pd

from .FeatureDescription import FeatureDescription


class Model:
    name: str
    handler: any
    filename: str

    def __init__(self, filename: str, handler: any = None, name: str = ""):
        self.name = name
        self.handler = handler

        self.filename = filename
        if filename:
            self.load(filename)

    def load(self, path: str) -> "Model": ...

    @staticmethod
    def supported_frameworks() -> list[str]: ...

    @classmethod
    def get_locale_filepath(cls, name: str = None) -> str:
        if name is None and hasattr(cls, "name"):
            name = cls.name
        return os.path.join(os.getenv("TEMP"), name, name)

    def get_feature_importance(
        self, feature_names: list[FeatureDescription], shap_values: np.array
    ) -> pd.DataFrame: ...

    def __repr__(self) -> str:
        return 'Model(name="{}", filename="{}")'.format(self.name, self.filename)
