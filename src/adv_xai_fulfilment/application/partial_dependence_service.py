import logging

from ..domain.model.model import Model
from ..infrastructure.constants import Errors
from ..domain.model.model_data import ModelData
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import PartialDependence
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
        selected_model: Model = self._model_loader_service.load_from(request, meta_data)
        if not selected_model.is_ok():
            logging.error("empty model")
            raise Errors.MODEL_NOT_MODEL

        logging.debug(f"downloading {request.data} data if present")
        data: ModelData = self._data_loader_service.load_data(request)

        if feature not in meta_data.feature_names:
            raise Exception(f"Feature {feature} not found in the model")

        return selected_model.get_partial_dependence(data.x, feature)
