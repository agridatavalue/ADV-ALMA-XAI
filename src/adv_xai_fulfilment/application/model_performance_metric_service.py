from logger import get_logger
from ..domain.model.model import Model
from ..domain.model.model_data import ModelData
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import ModelPerformance
from ..infrastructure.service.data_loader_service import DataLoaderService
from ..infrastructure.service.model_loader_service import ModelLoaderService
from ..domain.model.explainers.response_data import ModelPerformanceMetrics
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService
from ..domain.service.model_performance_service_component import (
    ModelPerformanceServiceComponent,
)

logger = get_logger()

class ModelPerformanceMetricService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _mdm_service: ModelPerformanceServiceComponent
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._mdm_service = ModelPerformanceServiceComponent()
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> ModelPerformance:
        model_metadata: ModelMetaData = (
            self._metadata_loader_service.load_model_metadata(explainer_identifier)
        )
        if not explainer_identifier.prediction_target:
            logger.debug(
                f"empty prediction target, setting default as {model_metadata.first_target_name}"
            )
            explainer_identifier.prediction_target = model_metadata.first_target_name

        selected_model: Model = self._model_loader_service.load_from(explainer_identifier, model_metadata)

        data: ModelData = self._data_loader_service.load_data(explainer_identifier)
        data.calculate_x_and_y_predict_and_x_and_y_train(model_metadata.feature_names, model_metadata.target_names[0])

        pred_target_index = model_metadata.index_of_target_name(
            explainer_identifier.prediction_target
        )
        logger.debug(
            f"index {pred_target_index} for target {explainer_identifier.prediction_target}"
        )
        return self._mdm_service.get_data(
            data=data,
            model=selected_model,
            prediction_target_index=pred_target_index,
            prediction_target=explainer_identifier.prediction_target,
        )
        
    def get_metrics(
        self, explainer_identifier: ExplainerIdentifier
    ) -> ModelPerformanceMetrics:
        model_metadata: ModelMetaData = (
            self._metadata_loader_service.load_model_metadata(explainer_identifier)
        )
        if not explainer_identifier.prediction_target:
            explainer_identifier.prediction_target = model_metadata.first_target_name

        selected_model: Model = self._model_loader_service.load_from(explainer_identifier, model_metadata)

        data: ModelData = self._data_loader_service.load_data(explainer_identifier)

        return self._mdm_service.get_metrics(
            prediction_target=explainer_identifier.prediction_target,
            model_metadata=model_metadata,
            model=selected_model,
            data=data,
        )
