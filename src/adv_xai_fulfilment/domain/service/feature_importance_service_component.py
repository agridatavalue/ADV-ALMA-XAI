import numpy as np
import pandas as pd

from logger import get_logger
from ..model.model import Model
from ..model.model_data import ModelData
from ..model.model_metadata import ModelMetaData
from .explainer_retriever import ExplainerRetriever
from ..model.explainer_metadata import ExplainerMetaData
from ..model.explainer_identifier import ExplainerIdentifier
from ..model.explainers.response_data import FeatureImportance
from ...infrastructure.service.DataLoaderService import DataLoaderService
from ...infrastructure.service.ModelLoaderService import ModelLoaderService
from ...infrastructure.service.MetaDataLoaderService import MetaDataLoaderService
from .feature_description_service_component import FeatureDescriptionServiceComponent
from ...infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)

logger = get_logger()

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
        logger.info(f"Generating feature importance for {explainer_identifier}")
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            explainer_identifier
        )

        selected_model: Model = self._model_loader_service.load_from(explainer_identifier, meta_data)

        if not explainer_identifier.prediction_target:
            logger.debug(
                "No prediction target provided, setting {meta_data.first_target_name}"
            )
            explainer_identifier.prediction_target = meta_data.first_target_name

        logger.debug(f"Prediction target: {explainer_identifier.prediction_target}")

        explainer = None
        explainer_identifier.category = meta_data.model_category
        for expl in self._explainer_retriever.get_for_feature_importance():
            logger.debug(f"Trying explainer: {expl}")
            try:
                path: str = self._explainer_repository_service.download_from(
                    explainer_identifier=explainer_identifier,
                    explainer=expl,
                )
                expl.load(path)
                explainer = expl

            except Exception as e:
                logger.warning(f"Error downloading explainer {expl}: {e}", exc_info=True)
                continue

        if not explainer:
            logger.error("No explainer found for feature importance")
            return FeatureImportance(
                feature=[],
                importance=[],
                prediction_target=explainer_identifier.prediction_target,
            )

        logger.info(f"Explainer feature-importance: {explainer}")

        model_data: ModelData = self._data_loader_service.load(
            explainer_identifier, meta_data.data_type
        )

        data: pd.DataFrame = selected_model.get_feature_importance(
            feature_names=self._feature_description_service.get_data(
                explainer_identifier
            ),
            shap_values=explainer.get_shap_values(
                x_test=np.array(model_data.x_train[meta_data.feature_names])
            ),
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
    ) -> FeatureImportance:

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
