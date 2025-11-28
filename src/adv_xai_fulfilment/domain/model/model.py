import numpy as np
import pandas as pd

from logger import get_logger

from .model_metadata import ModelMetaDataLayer
from .explainers.response_data import FeatureDescription


logger = get_logger()

class Model:
    name: str
    handler: object
    filename: str
    
    def __init__(self, filename: str, layers: list[ModelMetaDataLayer], name: str = ""):
        self.name = name
        self.handler = None

        self.filename = filename
        if filename:
            self.load({'path':filename, 'layers': layers})

    def load(self, data: dict) -> "Model": ...
    
    def predict(self, X):
        raise NotImplementedError
    
    def predict_proba(self, X):
        return self.handler.predict_proba(X)

    def is_ok(self) -> bool:
        return self.handler is not None
    
    @staticmethod
    def can_handle_federated() -> bool:
        return False
    
    @staticmethod
    def supported_frameworks() -> list[str]: ...
    
    def get_feature_importance(self, feature_names: list[FeatureDescription], shap_values: np.ndarray) -> pd.DataFrame:
        logger.debug(f"feature_names: {feature_names}, shap_values shape: {shap_values.shape}")
        shap_values = shap_values.reshape(-1, len(feature_names))
        mean_abs_shap_values = np.mean(np.abs(shap_values), axis=0) 
        
        if len(feature_names) != len(mean_abs_shap_values):
            logger.error(f"Feature names: {len(feature_names)}, SHAP values: {len(mean_abs_shap_values)}")
            return pd.DataFrame({ "Feature": [], "Importance": [] })

        return pd.DataFrame({
            "Feature": [f.name for f in feature_names],
            "Importance": mean_abs_shap_values.flatten(),
        }).sort_values(by="Importance", ascending=False).reset_index(drop=True)

    def __repr__(self) -> str:
        return '{}(name="{}", filename="{}")'.format(
            self.__class__.__name__, self.name, self.filename
        )
