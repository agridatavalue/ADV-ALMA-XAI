from ..model.ModelMetaData import ModelMetaData
from ..model.FeatureDescription import FeatureDescription
from ..model.ExplainerIdentifier import ExplainerIdentifier
from ...infrastructure.service.MetaDataLoaderService import MetaDataLoaderService


class FeatureDescriptionServiceComponent:
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> list[FeatureDescription]:
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            explainer_identifier=explainer_identifier
        )
        return meta_data.feature_descriptions
