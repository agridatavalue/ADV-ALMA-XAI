import numpy as np
import pandas as pd
from keras.models import load_model

from ..Model import Model
from ..FeatureDescription import FeatureDescription


class KerasModel(Model):

    def load(self, path: str) -> "KerasModel":
        self.handler = load_model(path)
        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["keras", "tensorflow", "tensorflow-keras"]

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
