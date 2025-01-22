import logging

from ..domain.model.Model import Model
from ..infrastructure.Constants import Errors
from ..domain.model.ModelData import ModelData
from ..domain.model.ModelMetaData import ModelMetaData
from ..domain.model.PartialDependence import PartialDependence
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService


class PartialDependenceService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, request: ExplainerIdentifier, feature: str) -> PartialDependence:
        logging.debug(f"downloading meta_data {request.metadata_identifier}")
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=request
        )
        request.metadata = meta_data

        logging.debug(f"downloading model {request.model}")
        selected_model: Model = self._model_loader_service.load_from(
            model_file_path=request.model, meta_data=meta_data
        )
        if not selected_model.is_ok():
            logging.error("empty model")
            raise Errors.MODEL_NOT_MODEL

        logging.debug(f"downloading {request.data} data if present")
        data: ModelData = self._data_loader_service.load_data(request)

        if feature not in meta_data.feature_names:
            raise Exception(f"Feature {feature} not found in the model")

        return selected_model.get_partial_dependence(data.x, feature)
