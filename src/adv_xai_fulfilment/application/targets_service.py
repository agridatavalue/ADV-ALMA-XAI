from ..domain.model.model_data import ModelData
from ..domain.model.explainer_metadata import ExplainerMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..domain.model.explainers.response_data import Targets, FeatureImportance
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService

class TargetsService:
    _data_loader_service: DataLoaderService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, expl_id: ExplainerIdentifier) -> Targets:
        data: ModelData = self._data_loader_service.load_data(expl_id)

        meta_data: ExplainerMetaData = (
            self._metadata_loader_service.load_explainer_metadata(expl_id)
        )

        feature = meta_data.feature_importance.get_most_important()