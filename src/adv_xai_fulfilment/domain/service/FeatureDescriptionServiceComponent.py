from ..model import ModelMetaData, ExplainerIdentifier
from ..model.explainers.responseData import FeatureDescription
from ...infrastructure.service.MetaDataLoaderService import MetaDataLoaderService


class FeatureDescriptionServiceComponent:
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> list[FeatureDescription]:
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=explainer_identifier
        )
        return meta_data.feature_descriptions
