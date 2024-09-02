import os
import logging
import numpy as np
import pandas as pd

from ..domain.model.Model import Model
from ..domain.model.explainers.Explainer import Explainer
from ..domain.service.ExplainerRetriever import ExplainerRetriever
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService


class FeatureImportanceService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _explainer_retriever: ExplainerRetriever

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._explainer_retriever = ExplainerRetriever()
        self._model_loader_service = ModelLoaderService()

    def genarate_data(self, model_filename: str, meta_data_filename: str) -> np.array:
        selected_model: Model = self._model_loader_service.load_from(model_filename)
        meta_data: dict = self._data_loader_service.load_meta_data(meta_data_filename)

        X_test = np.array(
            self._data_loader_service.load_data(
                bucket_name=os.getenv("DATA_FOLDER_PATH"), file_path="crop"
            )["x"]
        )

        x_train = np.array(
            self._data_loader_service.load_file(
                bucket_name=os.getenv("DATA_FOLDER_PATH"),
                file_path="X_background.csv",
            )
        )

        possible_explainers: list[Explainer] = self._explainer_retriever.get_by_data(
            selected_model=selected_model, meta_data=meta_data
        )

        logging.info(
            f"found {len(possible_explainers)} possible explainers: {possible_explainers}"
        )

        for explainer in possible_explainers:
            try:
                logging.debug("using explainer: %s" % explainer)
                if hasattr(explainer, "get_shap_values"):
                    return explainer.get_shap_values(
                        model=selected_model, x_test=X_test, x_train=x_train
                    )

                raise Exception("Explainer does not have a get_shap_values method")
            except Exception as e:
                logging.info(
                    f"Discarded explainer {explainer.name} because of error: {e}"
                )

    def genarate_feature_description(self, meta_data_filename: str) -> dict:
        meta_data: dict = self._data_loader_service.load_meta_data(meta_data_filename)
        return meta_data.get("feature_descriptions", {})
