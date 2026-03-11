import pickle
from os import path
from abc import ABC
from typing import Optional

from logger import get_logger
from ..domain.model.model import Model
from ..infrastructure.constants import Errors
from ..domain.model.model_data import ModelData
from ..domain.model.model_context import ModelContext
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainers.explainer import Explainer
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.data_loader_service import DataLoaderService
from ..infrastructure.service.model_loader_service import ModelLoaderService
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService

logger = get_logger()

class AbstractModelService(ABC):
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _metadata_loader_service: MetaDataLoaderService
    
    def __init__(
        self, 
        data_loader_service: Optional[DataLoaderService] = None, 
        model_loader_service: Optional[ModelLoaderService] = None, 
        metadata_loader_service: Optional[MetaDataLoaderService] = None
    ):
        self._data_loader_service = data_loader_service or DataLoaderService()
        self._model_loader_service = model_loader_service or ModelLoaderService()
        self._metadata_loader_service = metadata_loader_service or MetaDataLoaderService()
        
    def get_context(
        self, 
        explainer_identifier: ExplainerIdentifier, 
        force_download: bool = False
    ) -> ModelContext:
        if not explainer_identifier:
            raise ValueError("explainer_identifier is required")
        
        model_metadata: ModelMetaData = (
            self._metadata_loader_service.load_model_metadata(
                explainer_identifier, force_download=force_download
            )
        )
        if not explainer_identifier.prediction_target:
            logger.debug(
                f"empty prediction target, setting default as {model_metadata.first_target_name}"
            )
            explainer_identifier.prediction_target = model_metadata.first_target_name

        selected_model: Optional[Model] = self._model_loader_service.load_from(
            explainer_identifier, meta_data=model_metadata, force_download=force_download
        )
        
        if not (selected_model and selected_model.is_ok()):
            logger.error(f"empty model {explainer_identifier.model}")
            raise Errors.MODEL_NOT_MODEL

        data: ModelData = self._data_loader_service.load_data(
            explainer_identifier, 
            algorithm=model_metadata.algorithm,
            force_download=force_download,
        )
        if model_metadata.is_federated and model_metadata.is_deep_learning:
            data.calculate_federated_y_predict(
                model = selected_model, 
                metadata_layers = model_metadata.architectures,
            )
        else:
            data.calculate_x_and_y_predict_and_x_and_y_train(
                model = selected_model, 
                target_name = model_metadata.target_names[0],
                feature_names = model_metadata.feature_names, 
                model_category = model_metadata.model_category,
            )

        return ModelContext(
            model = selected_model,
            model_data = data,
            model_metadata = model_metadata,
            identifier = explainer_identifier
        )

    def _get_explanator(self, request: ExplainerIdentifier, explainer: Explainer) -> object:
        if not isinstance(explainer, Explainer):
            raise ValueError("explainer must be an instance of Explainer")

        explainer_filepath = request.get_explainer_locale_filepath(explainer)
        if not explainer_filepath:
            raise ValueError("Explainer filepath is empty")

        if not path.exists(explainer_filepath):
            raise ValueError(f"Explainer file does not exist: {explainer_filepath}")

        if path.getsize(explainer_filepath) == 0:
            raise ValueError(f"Explainer file is empty: {explainer_filepath}")

        try:
            with open(explainer_filepath, "rb") as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError) as e:
            raise ValueError(f"Failed to load explainer from {explainer_filepath}: {e}")

