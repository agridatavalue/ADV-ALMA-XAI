import joblib
import numpy as np
import pandas as pd

from ..model import Model
from ..explainers.response_data import FeatureDescription


class TabpfnModel(Model):
    def load(self, data: dict) -> "TabpfnModel":
        self.handler = joblib.load(data.get('path'))
        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["tabpfn", "tab-pfn"]
    
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

