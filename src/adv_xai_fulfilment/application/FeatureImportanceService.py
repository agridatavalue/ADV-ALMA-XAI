from ..domain.model.ModelMetaData import ModelMetaData
from ..domain.model.ExplainerMetaData import ExplainerMetaData
from ..domain.model.FeatureDescription import FeatureDescription
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..domain.service.FeatureImportanceServiceComponent import (
    FeatureImportanceServiceComponent,
)


class FeatureImportanceService:
    _data_loader_service: DataLoaderService
    _feature_importance_service_comp: FeatureImportanceServiceComponent

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._feature_importance_service_comp = FeatureImportanceServiceComponent()

    def get_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> dict[
        "Feature" : list[str],
        "Importance" : list[float],
        "prediction_target":str,
    ]:
        meta_data: ExplainerMetaData = (
            self._data_loader_service.load_explainer_metadata(explainer_identifier)
        )
        return meta_data.feature_importance

    def genarate_feature_description(
        self, explainer_identifier: ExplainerIdentifier
    ) -> list[FeatureDescription]:
        meta_data: ModelMetaData = self._data_loader_service.load_model_metadata(
            explainer_identifier=explainer_identifier
        )
        return meta_data.feature_descriptions
