from ..domain.model.explainers.response_data import Heatmap
from ..domain.model.explainer_metadata import ExplainerMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService


class HeatmapService:
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, expl_id: ExplainerIdentifier) -> Heatmap:
        meta_data: ExplainerMetaData = (
            self._metadata_loader_service.load_explainer_metadata(expl_id)
        )
        return meta_data.heatmap
