from ..domain.model.model import Model
from ..domain.model.model_data import ModelData
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainers.response_data import Targets
from ..domain.model.explainer_metadata import ExplainerMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService

class TargetsService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, expl_id: ExplainerIdentifier) -> Targets:
        data: ModelData = self._data_loader_service.load_data(expl_id)

        model_metadata: ModelMetaData = (
            self._metadata_loader_service.load_model_metadata(expl_id)
        )
        selected_model: Model = self._model_loader_service.load_from(expl_id, model_metadata)

        meta_data: ExplainerMetaData = (
            self._metadata_loader_service.load_explainer_metadata(expl_id)
        )
        feature:str = meta_data.feature_importance.get_most_important()

        predicted_y = selected_model.handler.predict(data.x)
        return Targets().set_x(data.x[feature]).set_y(real=data.y, predicted=predicted_y)
