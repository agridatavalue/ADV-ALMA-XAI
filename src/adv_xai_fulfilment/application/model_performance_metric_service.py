from logger import get_logger
from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import ModelPerformance
from ..domain.model.explainers.response_data import ModelPerformanceMetrics
from ..domain.service.model_performance_service_component import (
    ModelPerformanceServiceComponent,
)
logger = get_logger()

class ModelPerformanceMetricService(AbstractModelService):
    _mdm_service: ModelPerformanceServiceComponent

    def __init__(self):
        super().__init__()
        self._mdm_service = ModelPerformanceServiceComponent()

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> ModelPerformance:
        context = self.get_context(explainer_identifier)
        
        pred_target_index = context.model_metadata.index_of_target_name(
            explainer_identifier.prediction_target
        )
        logger.debug(
            f"index {pred_target_index} for target {explainer_identifier.prediction_target}"
        )
        return self._mdm_service.get_data(
            data=context.model_data,
            model=context.model,
            prediction_target_index=pred_target_index,
            prediction_target=explainer_identifier.prediction_target,
        )
        
    def get_metrics(self, explainer_identifier: ExplainerIdentifier) -> ModelPerformanceMetrics:
        context = self.get_context(explainer_identifier)
        
        return self._mdm_service.get_metrics(
            prediction_target = explainer_identifier.prediction_target,
            model_metadata = context.model_metadata,
            model = context.model,
            data = context.model_data,
        )
