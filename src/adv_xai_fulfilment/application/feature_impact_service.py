import numpy as np
from typing import Optional

from logger import get_logger
from .abstract_model_service import AbstractModelService
from ..domain.model.explainers.response_data import FeatureImpact
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.service.explainer_retriever import ExplainerRetriever
from ..infrastructure.service.explainer_repository_service import ExplainerRepositoryService

logger = get_logger()

class FeatureImpactService(AbstractModelService):
    _explainer_retriever: ExplainerRetriever
    _explainer_repository_service: ExplainerRepositoryService

    def __init__(self):
        super().__init__()
        self._explainer_retriever = ExplainerRetriever()
        self._explainer_repository_service = ExplainerRepositoryService()

    def get_data(
        self, explainer_identifier: ExplainerIdentifier, requested_feature: str = ""
    ) -> FeatureImpact:
        context = self.get_context(explainer_identifier)
        
        features_to_explain: list[str] = context.model_metadata.feature_names
        if requested_feature:
            features_to_explain = [requested_feature]
        
        to_return = FeatureImpact()
        explainer = None
        for expl in self._explainer_retriever.get_for_feature_importance(context.model_metadata.algorithm):
            logger.debug(f"Trying explainer: {expl}")
            try:
                path: str = self._explainer_repository_service.download_from(
                    explainer_identifier=context.identifier,
                    explainer=expl,
                )
                expl.load(path) 
                explainer = expl

                for feature in features_to_explain:
                    to_return = to_return.with_feature(feature).set_data(
                        explainer.get_shap_values(
                            x_test=np.array(context.model_data.x_train[context.model_metadata.feature_names])
                        )
                    )
                return to_return

            except Exception as e:
                logger.warning(f"Error downloading explainer {expl}: {e}")
                continue

        if not explainer:
            logger.error("No explainer found for feature impact")
        
        return to_return
