import os
import logging
import numpy as np
import pandas as pd

from ..domain.service.ExplainerRetriever import ExplainerRetriever
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)


class FeatureImportanceService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _explainer_retriever: ExplainerRetriever
    _explainer_repository_service: ExplainerRepositoryService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._explainer_retriever = ExplainerRetriever()
        self._model_loader_service = ModelLoaderService()
        self._explainer_repository_service = ExplainerRepositoryService()

    def get_data(self, meta_data_filename: str, pilot: str) -> pd.DataFrame:
        explainer = None
        for expl in self._explainer_retriever.get_for_feature_importance():
            try:
                path: str = self._explainer_repository_service.download(pilot, expl)
                expl.load(path)
                explainer = expl

            except Exception as e:
                logging.error(
                    f"Error downloading explainer: {e.message if hasattr(e, 'message') else str(e)}"
                )
                continue

        if not explainer:
            logging.error("No explainer found for feature importance")
            return pd.DataFrame([{"Feature": [], "Importance": []}])

        logging.info(f"Explainer feature-importance: {explainer}")
        feature_names = list(
            self.genarate_feature_description(meta_data_filename).keys()
        )

        X_test = np.array(
            self._data_loader_service.load_data(
                bucket_name=os.getenv("DATA_FOLDER_PATH"), folder_path="crop"
            )["x"]
        )

        shap_values: np.array = explainer.get_shap_values(x_test=X_test)
        mean_abs_shap_values = np.mean(np.abs(shap_values), axis=0)
        return pd.DataFrame(
            [
                {
                    "Feature": feature_names,
                    "Importance": mean_abs_shap_values.tolist(),
                }
            ]
        )

    def genarate_feature_description(self, meta_data_filename: str) -> dict:
        meta_data: dict = self._data_loader_service.load_meta_data(meta_data_filename)
        return meta_data.get("feature_descriptions", {}) if meta_data else {}
