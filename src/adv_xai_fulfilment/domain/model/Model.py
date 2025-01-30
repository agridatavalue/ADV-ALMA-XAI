import os
import numpy as np
import pandas as pd
from tqdm import tqdm

from .explainers.responseData.PartialDependence import PartialDependence
from .explainers.responseData.FeatureDescription import FeatureDescription


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

    def is_ok(self) -> bool:
        return self.handler is not None

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

    def get_partial_dependence(
        self, X: pd.DataFrame, feature: str
    ) -> PartialDependence:
        num_points = len(X)

        if hasattr(X, "columns"):
            feature_names = X.columns
        else:
            feature_names = [f"Feature {i}" for i in range(X.shape[1])]

        # Convert X to numpy array if it's a DataFrame
        if hasattr(X, "values"):
            X = X.values

        # Get feature index
        if isinstance(feature, str):
            feature_idx = list(feature_names).index(feature)
        else:
            feature_idx = feature
            feature = feature_names[feature_idx]

        # Get feature values range (1st to 99th percentile)
        feature_values = np.linspace(
            np.percentile(X[:, feature_idx], 1),
            np.percentile(X[:, feature_idx], 99),
            num_points,
        )

        # Calculate mean predictions
        predictions = []
        for value in tqdm(feature_values, desc=f"Processing {feature}"):
            X_temp = X.copy()
            X_temp[:, feature_idx] = value
            pred = self.handler.predict(X_temp)
            predictions.append(np.mean(pred))

        return PartialDependence(
            feature_values=feature_values,
            std_effect=np.std(predictions),
            pdp_values=np.array(predictions),
            mean_effect=np.mean(np.abs(np.array(predictions) - np.mean(predictions))),
        )
