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
        self, feature_names: list[FeatureDescription], shap_values: np.ndarray
    ) -> pd.DataFrame:
        mean_abs_shap_values = np.mean(np.abs(shap_values), axis=0)

        return (
            pd.DataFrame({
                "Feature": [f.name for f in feature_names],
                "Importance": mean_abs_shap_values.flatten(),
            })
            .sort_values(by="Importance", ascending=False)
            .reset_index(drop=True)
        )

