from ..model.ModelMetaData import ModelMetaData
from ..model.FeatureDescription import FeatureDescription
from ..model.ExplainerIdentifier import ExplainerIdentifier
from ...infrastructure.service.DataLoaderService import DataLoaderService


class FeatureDescriptionServiceComponent:
    _data_loader_service: DataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()

    def get_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> list[FeatureDescription]:
        meta_data: ModelMetaData = self._data_loader_service.load_model_metadata(
            explainer_identifier=explainer_identifier
        )
        return meta_data.feature_descriptions
