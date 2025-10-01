import numpy as np
import pandas as pd

from logger import get_logger
from ..model.model_context import ModelContext
from .explainer_retriever import ExplainerRetriever
from ..model.explainer_metadata import ExplainerMetaData
from ..model.explainer_identifier import ExplainerIdentifier
from ..model.explainers.response_data import FeatureImportance
from ...infrastructure.service.metadata_loader_service import MetaDataLoaderService
from .feature_description_service_component import FeatureDescriptionServiceComponent
from ...infrastructure.service.explainer_repository_service import (
    ExplainerRepositoryService,
)

logger = get_logger()

class FeatureImportanceServiceComponent:
    _explainer_retriever: ExplainerRetriever
    _metadata_loader_service = MetaDataLoaderService()
    _explainer_repository_service: ExplainerRepositoryService
    _feature_description_service: FeatureDescriptionServiceComponent

    def __init__(self):
        self._explainer_retriever = ExplainerRetriever()
        self._metadata_loader_service = MetaDataLoaderService()
        self._explainer_repository_service = ExplainerRepositoryService()
        self._feature_description_service = FeatureDescriptionServiceComponent()

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> FeatureImportance:
        meta_data: ExplainerMetaData = (
            self._metadata_loader_service.load_explainer_metadata(explainer_identifier)
        )
        return meta_data.feature_importance

    def generate_data(self, context: ModelContext) -> FeatureImportance:
        explainer = None
        data_to_return = {"Feature": pd.DataFrame(), "Importance": pd.DataFrame()}
        for expl in self._explainer_retriever.get_for_feature_importance(context.model_metadata.algorithm):
            logger.debug(f"Trying explainer: {expl}")
            try:
                path: str = self._explainer_repository_service.download_from(
                    explainer_identifier=context.identifier,
                    explainer=expl,
                )
                expl.load(path)
                explainer = expl
                
                data_to_return = context.model.get_feature_importance(
                    feature_names=self._feature_description_service.get_data(
                        context.identifier
                    ),
                    shap_values=explainer.get_shap_values(
                        x_test=np.array(context.model_data.x_train[context.model_metadata.feature_names])
                    ),
                )

            except Exception as e:
                logger.warning(f"Error downloading explainer {expl}: {e}")
                continue

        if not explainer:
            logger.error("No explainer found for feature importance")
            return FeatureImportance(
                feature=[],
                importance=[],
                prediction_target=context.identifier.prediction_target,
            )

        return self.__prepare_data(
            data=data_to_return,
            prediction=context.identifier.prediction_target,
            target_names=context.model_metadata.target_names,
        )

    def __prepare_data(
        self,
        prediction: str,
        data: dict["Feature" : pd.DataFrame, "Importance" : pd.DataFrame],
        target_names: list[str],
    ) -> FeatureImportance:
        if not isinstance(data, dict) or "Feature" not in data or "Importance" not in data:
            raise ValueError("Invalid data format for feature importance")
        if (
            not isinstance(data["Feature"], (pd.DataFrame, np.ndarray)) 
            or not isinstance(data["Importance"], (pd.DataFrame, np.ndarray))
        ): raise ValueError(
            f"'Feature' and 'Importance' data keys has to be DataFrame or numpy arrays got: {type(data['Feature'])}, {type(data['Importance'])}"
        )
            
        to_ret = FeatureImportance(
            prediction_target=prediction,
            feature=(
                data["Feature"].tolist()
                if isinstance(data["Feature"], np.ndarray) 
                else data["Feature"]
            ),
            importance=(
                data["Importance"].tolist() 
                if isinstance(data["Importance"], np.ndarray) 
                else data["Importance"]
            ),
        )

        if len(to_ret.importance) > 0 and isinstance(to_ret.importance[0], list):
            to_ret.importance = [
                d[target_names.index(prediction)] for d in to_ret.importance[0]
            ]
        return to_ret
