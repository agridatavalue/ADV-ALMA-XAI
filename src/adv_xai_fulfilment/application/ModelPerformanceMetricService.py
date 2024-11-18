import os
import pandas as pd

from ..domain.model.Model import Model
from ..domain.model.ModelMetaData import ModelMetaData
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

    def get_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> dict["target":str, "y_pred" : pd.DataFrame, "y_true" : pd.DataFrame]:
        selected_model: Model = self._model_loader_service.load_from(
            explainer_identifier.model
        )

        data: dict = self._data_loader_service.load_data(
            bucket_name=os.getenv("DATA_FOLDER_PATH"),
            folder_path=explainer_identifier.data,
        )

        model_metadata: ModelMetaData = self._data_loader_service.load_model_metadata(
            explainer_identifier
        )
        if not explainer_identifier.prediction_target:
            explainer_identifier.prediction_target = model_metadata.first_target_name

        model_performance: dict = self._mdm_service.get_data(
            data=data,
            model=selected_model,
            prediction_target_index=model_metadata.index_of_target_name(
                explainer_identifier.prediction_target
            ),
        )
        return {**model_performance, "target": explainer_identifier.prediction_target}

    def get_metrics(
        self, explainer_identifier: ExplainerIdentifier
    ) -> dict["x" : pd.DataFrame, "y" : pd.DataFrame]:
        selected_model: Model = self._model_loader_service.load_from(
            explainer_identifier.model
        )

        data: dict = self._data_loader_service.load_data(
            bucket_name=os.getenv("DATA_FOLDER_PATH"),
            folder_path=explainer_identifier.model,
        )

        model_metadata: ModelMetaData = self._data_loader_service.load_model_metadata(
            explainer_identifier
        )
        if not explainer_identifier.prediction_target:
            explainer_identifier.prediction_target = model_metadata.first_target_name

        return self._mdm_service.get_metrics(
            model=selected_model,
            data=data,
            prediction_target_index=model_metadata.index_of_target_name(
                explainer_identifier.prediction_target
            ),
        )
