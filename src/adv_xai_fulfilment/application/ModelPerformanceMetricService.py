import os

from ..domain.model.Model import Model
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..domain.service.ModelPerformanceMetricServiceComponent import (
    ModelPerformanceMetricServiceComponent,
)


class ModelPerformanceMetricService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _mdm_service: ModelPerformanceMetricServiceComponent

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()
        self._mdm_service = ModelPerformanceMetricServiceComponent()

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> dict:
        selected_model: Model = self._model_loader_service.load_from(
            explainer_identifier.model
        )

        data: dict = self._data_loader_service.load_data(
            bucket_name=os.getenv("DATA_FOLDER_PATH"),
            folder_path=explainer_identifier.data,
        )

        return self._mdm_service.get_data(
            data=data,
            model=selected_model,
            prediction_target_index=explainer_identifier.prediction_target,
        )

    def get_metrics(self, prediction_target: int, model_filename: str) -> dict:
        selected_model: Model = self._model_loader_service.load_from(model_filename)

        data: dict = self._data_loader_service.load_data(
            bucket_name=os.getenv("DATA_FOLDER_PATH"), folder_path="crop"
        )

        return self._mdm_service.get_metrics(
            model=selected_model, data=data, prediction_target=prediction_target
        )
