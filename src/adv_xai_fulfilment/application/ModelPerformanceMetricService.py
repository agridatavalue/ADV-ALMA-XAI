import logging

from ..domain.model.Model import Model
from ..domain.model.ModelData import ModelData
from ..domain.model.ModelMetaData import ModelMetaData
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService
from ..domain.model.explainers.responseData.ModelPerformance import ModelPerformance
from ..domain.service.ModelPerformanceServiceComponent import (
    ModelPerformanceServiceComponent,
)
from ..domain.model.explainers.responseData.ModelPerformanceMetrics import (
    ModelPerformanceMetrics,
)


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
            logging.debug(
                f"empty prediction target, setting default as {model_metadata.first_target_name}"
            )
            explainer_identifier.prediction_target = model_metadata.first_target_name

        selected_model: Model = self._model_loader_service.load_from(
            explainer_identifier.model, meta_data=model_metadata
        )

        data: ModelData = self._data_loader_service.load_data(explainer_identifier)

        pred_target_index = model_metadata.index_of_target_name(
            explainer_identifier.prediction_target
        )
        logging.debug(
            f"index {pred_target_index} for target {explainer_identifier.prediction_target}"
        )
        mp: ModelPerformance = self._mdm_service.get_data(
            data=data,
            model=selected_model,
            prediction_target_index=pred_target_index,
        )
        mp.target = explainer_identifier.prediction_target
        return mp

    def get_metrics(
        self, explainer_identifier: ExplainerIdentifier
    ) -> ModelPerformanceMetrics:
        model_metadata: ModelMetaData = (
            self._metadata_loader_service.load_model_metadata(explainer_identifier)
        )
        if not explainer_identifier.prediction_target:
            explainer_identifier.prediction_target = model_metadata.first_target_name

        selected_model: Model = self._model_loader_service.load_from(
            explainer_identifier.model, meta_data=model_metadata
        )

        data: ModelData = self._data_loader_service.load_data(explainer_identifier)

        return self._mdm_service.get_metrics(
            prediction_target=explainer_identifier.prediction_target,
            model_metadata=model_metadata,
            model=selected_model,
            data=data,
        )
