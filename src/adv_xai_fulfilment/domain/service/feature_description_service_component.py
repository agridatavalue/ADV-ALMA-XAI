from ..model.model_metadata import ModelMetaData
from ..model.explainer_identifier import ExplainerIdentifier
from ..model.explainers.response_data import FeatureDescription
from ...infrastructure.service.metadata_loader_service import MetaDataLoaderService


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
        if meta_data.feature_descriptions:
            return [
                f for f in meta_data.feature_descriptions if f.name in meta_data.feature_names
            ]

        return [FeatureDescription(name=f) for f in meta_data.feature_names]
