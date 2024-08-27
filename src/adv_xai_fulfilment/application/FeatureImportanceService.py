import shap
import numpy as np
import pandas as pd

from ..domain.model.Model import Model
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService


class FeatureImportanceService:
    data_loader_service: DataLoaderService
    model_loader_service: ModelLoaderService

    def __init__(self):
        self.data_loader_service = DataLoaderService()
        self.model_loader_service = ModelLoaderService()

    def genarate_data_for_pilot(self, model_file_name: str) -> dict:
        model: Model = self.model_loader_service.load_from(model_file_name)

        # Extract X_test from the request
        X_test: pd.DataFrame = np.array(
            self.data_loader_service.load_data("datagen/crop")["x"]
        )
        # Initialize SHAP explainer
        explainer = shap.DeepExplainer(model.handler, X_test)
        # Compute SHAP values
        shap_values = explainer.shap_values(X_test)
        # Summarize feature importance (average absolute SHAP values per feature)
        return np.mean(np.abs(shap_values), axis=0)
