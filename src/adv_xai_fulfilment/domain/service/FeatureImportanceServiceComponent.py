import logging
import numpy as np
import pandas as pd

from ...domain.model.Model import Model
from ...domain.model.ModelData import ModelData
from ...domain.model.ModelMetaData import ModelMetaData
from ...domain.model.ExplainerMetaData import ExplainerMetaData
from ...domain.model.FeatureImportance import FeatureImportance
from ...domain.model.ExplainerIdentifier import ExplainerIdentifier
from ...domain.service.ExplainerRetriever import ExplainerRetriever
from ...infrastructure.service.DataLoaderService import DataLoaderService
from ...infrastructure.service.ModelLoaderService import ModelLoaderService
from ...infrastructure.service.MetaDataLoaderService import MetaDataLoaderService
from .FeatureDescriptionServiceComponent import FeatureDescriptionServiceComponent
from ...infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)


class FeatureImportanceServiceComponent:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _explainer_retriever: ExplainerRetriever
    _metadata_loader_service = MetaDataLoaderService()
    _explainer_repository_service: ExplainerRepositoryService
    _feature_description_service: FeatureDescriptionServiceComponent

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._explainer_retriever = ExplainerRetriever()
        self._model_loader_service = ModelLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()
        self._explainer_repository_service = ExplainerRepositoryService()
        self._feature_description_service = FeatureDescriptionServiceComponent()

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> FeatureImportance:
        meta_data: ExplainerMetaData = (
            self._metadata_loader_service.load_explainer_metadata(explainer_identifier)
        )
        return meta_data.feature_importance

    def generate_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> FeatureImportance:
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
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
            return FeatureImportance(
                feature=[],
                importance=[],
                prediction_target=explainer_identifier.prediction_target,
            )

        logging.info(f"Explainer feature-importance: {explainer}")

        model_data: ModelData = self._data_loader_service.load_data(
            explainer_identifier
        )

        data: pd.DataFrame = selected_model.get_feature_importance(
            feature_names=self._feature_description_service.get_data(
                explainer_identifier
            ),
            shap_values=explainer.get_shap_values(x_test=np.array(model_data.x)),
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

        to_ret = FeatureImportance(
            prediction_target=prediction,
            feature=data["Feature"].tolist(),
            importance=data["Importance"].tolist(),
        )

        if len(to_ret.importance) > 0 and isinstance(to_ret.importance[0], list):
            to_ret.importance = [
                d[target_names.index(prediction)] for d in to_ret.importance[0]
            ]
        return to_ret
