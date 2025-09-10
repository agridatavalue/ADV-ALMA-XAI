from logger import get_logger
from ..domain.model.model import Model
from ..infrastructure.constants import Errors
from ..domain.model.model_data import ModelData
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.data_loader_service import DataLoaderService
from ..infrastructure.service.model_loader_service import ModelLoaderService
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService
from ..domain.model.explainers.response_data import IndividualConditionalExpectations

logger = get_logger()

class IndividualConditionalExpectationService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, request:ExplainerIdentifier, feature: str) -> IndividualConditionalExpectations:
        logger.debug(f"downloading meta_data {request.metadata_identifier}")
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=request
        )
        request.metadata = meta_data

        logger.debug(f"downloading model {request.model}")
        selected_model: Model = self._model_loader_service.load_from(request, meta_data)
        if not selected_model.is_ok():
            logger.error("empty model")
            raise Errors.MODEL_NOT_MODEL

        logger.debug(f"downloading {request.data} data if present")
        data: ModelData = self._data_loader_service.load_data(request)

        data.remove_columns_not_in_model(meta_data.feature_names)

        if feature not in meta_data.feature_names:
            raise Exception(f"Feature {feature} not found in the model")

        return selected_model.get_individual_conditional_expectations(data.x, feature)