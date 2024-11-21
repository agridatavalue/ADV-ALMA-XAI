import os
import logging
import numpy as np
import pandas as pd

from ...domain.model.Model import Model
from ...domain.model.ModelMetaData import ModelMetaData
from ...domain.model.ExplainerIdentifier import ExplainerIdentifier
from ...domain.service.ExplainerRetriever import ExplainerRetriever
from ...infrastructure.service.DataLoaderService import DataLoaderService
from ...infrastructure.service.ModelLoaderService import ModelLoaderService
from ...infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)


class FeatureImportanceServiceComponent:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _explainer_retriever: ExplainerRetriever
    _explainer_repository_service: ExplainerRepositoryService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._explainer_retriever = ExplainerRetriever()
        self._model_loader_service = ModelLoaderService()
        self._explainer_repository_service = ExplainerRepositoryService()

    def get_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> dict[
        "Feature" : list[str],
        "Importance" : list[float],
        "prediction_target":str,
    ]:
        meta_data: ModelMetaData = self._data_loader_service.load_model_metadata(
            explainer_identifier
        )
        selected_model: Model = self._model_loader_service.load_from(
            model_file_path=explainer_identifier.model, meta_data=meta_data
        )

        if not explainer_identifier.prediction_target:
            explainer_identifier.prediction_target = meta_data.first_target_name

        logging.debug(f"Prediction target: {explainer_identifier.prediction_target}")

        explainer = None
        explainer_identifier.category = meta_data.model_category
        for expl in self._explainer_retriever.get_for_feature_importance():
            logging.debug(f"Trying explainer: {expl}")
            try:
                path: str = self._explainer_repository_service.download_from(
                    explainer_identifier=explainer_identifier,
                    explainer=expl,
                )
                expl.load(path)
                explainer = expl

            except Exception as e:
                logging.error(
                    f"Error downloading explainer: {e.message if hasattr(e, 'message') else str(e)}"
                )
                continue

        if not explainer:
            logging.error("No explainer found for feature importance")
            return {
                "Feature": [],
                "Importance": [],
                "prediction_target": explainer_identifier.prediction_target,
            }

        logging.info(f"Explainer feature-importance: {explainer}")

        X_test = np.array(
            self._data_loader_service.load_data(
                bucket_name=os.getenv("DATA_FOLDER_PATH"),
                folder_path=explainer_identifier.data,
            )["x"]
        )

        data: pd.DataFrame = selected_model.get_feature_importance(
            feature_names=self.genarate_feature_description(explainer_identifier),
            shap_values=explainer.get_shap_values(x_test=X_test),
        )
        return self.__prepare_data(
            data=data,
            prediction=explainer_identifier.prediction_target,
            target_names=meta_data.target_names,
        )

    def __prepare_data(
        self,
        prediction: str,
        data: dict["Feature" : pd.DataFrame, "Importance" : pd.DataFrame],
        target_names: list[str],
    ) -> dict:
        to_ret = {
            "Feature": data["Feature"].tolist(),
            "Importance": data["Importance"].tolist(),
            "prediction_target": prediction,
        }
        if len(to_ret["Importance"]) > 0 and isinstance(to_ret["Importance"][0], list):
            to_ret["Importance"] = [
                d[target_names.index(prediction)] for d in to_ret["Importance"][0]
            ]
        return to_ret
