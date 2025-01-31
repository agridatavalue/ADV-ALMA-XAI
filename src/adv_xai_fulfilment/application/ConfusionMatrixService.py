import logging

from ..domain.model.Model import Model
from ..domain.model.ModelData import ModelData
from ..domain.model.ModelMetaData import ModelMetaData
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService
from ..domain.model.explainers.responseData.ConfusionMatrix import ConfusionMatrix


class ConfusionMatrixService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> ConfusionMatrix:
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

        return selected_model.get_confusion_matrix(data)
