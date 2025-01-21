import pandas as pd

from ..domain.model.Model import Model
from ..domain.model.ModelData import ModelData
from ..domain.model.ModelMetaData import ModelMetaData
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService
from ..domain.service.ModelPerformanceServiceComponent import (
    ModelPerformanceServiceComponent,
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

    def get_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> dict["target":str, "y_pred" : pd.DataFrame, "y_true" : pd.DataFrame]:
        model_metadata: ModelMetaData = (
            self._metadata_loader_service.load_model_metadata(explainer_identifier)
        )
        if not explainer_identifier.prediction_target:
            explainer_identifier.prediction_target = model_metadata.first_target_name

        selected_model: Model = self._model_loader_service.load_from(
            explainer_identifier.model, meta_data=model_metadata
        )

        data: ModelData = self._data_loader_service.load_data(explainer_identifier)

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
            model=selected_model,
            data=data,
            prediction_target_index=model_metadata.index_of_target_name(
                explainer_identifier.prediction_target
            ),
        )
