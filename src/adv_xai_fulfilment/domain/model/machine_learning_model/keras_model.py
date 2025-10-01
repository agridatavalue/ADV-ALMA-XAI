import numpy as np
import pandas as pd
from tqdm import tqdm
from keras.models import load_model

from ..model import Model
from ..explainers.response_data import PartialDependence, FeatureDescription


class KerasModel(Model):
    def load(self, data: dict) -> "KerasModel":
        self.handler = load_model(data.get('path'))
        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["keras", "tensorflow", "tensorflow-keras"]
    
    def predict(self, X):
        return self.handler.predict(X)

    def get_feature_importance(
        self, feature_names: list[FeatureDescription], shap_values: np.array
    ) -> pd.DataFrame:
        mean_abs_shap_values = np.mean(np.abs(shap_values), axis=0)
        return pd.DataFrame(
            [
                {
                    "Feature": [f.name for f in feature_names],
                    "Importance": mean_abs_shap_values.tolist(),
                }
            ]
        )

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
            pred = self.handler.predict(X_temp, verbose=0)
            predictions.append(np.mean(pred))

        return PartialDependence(
            feature_values=feature_values,
            std_effect=np.std(predictions),
            pdp_values=np.array(predictions),
            mean_effect=np.mean(np.abs(np.array(predictions) - np.mean(predictions))),
        )
