from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..domain.model.explainers.responseData.FeatureDescription import FeatureDescription
from ..domain.service.FeatureDescriptionServiceComponent import (
    FeatureDescriptionServiceComponent,
)


class FeatureDescriptionService:
    _feature_description_service: FeatureDescriptionServiceComponent

    def __init__(self):
        self._feature_description_service = FeatureDescriptionServiceComponent()

    def get_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> list[FeatureDescription]:
        if not explainer_identifier.metadata_identifier:
            explainer_identifier.metadata_identifier = "metadata_v2.json"

        return self._feature_description_service.get_data(explainer_identifier)
