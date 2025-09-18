from typing import Optional

from logger import get_logger
from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import ModelPerformance
from ..domain.model.explainers.response_data import ModelPerformanceMetrics
from src.adv_xai_fulfilment.infrastructure.service.data_loader_service import DataLoaderService
from src.adv_xai_fulfilment.infrastructure.service.model_loader_service import ModelLoaderService
from src.adv_xai_fulfilment.infrastructure.service.metadata_loader_service import MetaDataLoaderService
from ..domain.service.model_performance_service_component import (
    ModelPerformanceServiceComponent,
)
logger = get_logger()

class ModelPerformanceMetricService(AbstractModelService):
    _mdm_service: ModelPerformanceServiceComponent

    def __init__(
        self,
        data_loader_service: Optional[DataLoaderService] = None, 
        model_loader_service: Optional[ModelLoaderService] = None, 
        metadata_loader_service: Optional[MetaDataLoaderService] = None
    ):
        super().__init__(
            data_loader_service=data_loader_service, 
            model_loader_service=model_loader_service, 
            metadata_loader_service=metadata_loader_service
        )
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
            data = context.model_data,
            prediction_target = explainer_identifier.prediction_target,
        )
        
    def get_metrics(self, explainer_identifier: ExplainerIdentifier) -> ModelPerformanceMetrics:
        context = self.get_context(explainer_identifier)
        
        return self._mdm_service.get_metrics(
            model_metadata = context.model_metadata,
            model = context.model,
            data = context.model_data,
        )
