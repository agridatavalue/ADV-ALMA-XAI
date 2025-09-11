from ..domain.service import FeatureDescriptionServiceComponent
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import FeatureDescription


class FeatureDescriptionService:
    _feature_description_service: FeatureDescriptionServiceComponent

    def __init__(self):
        self._feature_description_service = FeatureDescriptionServiceComponent()

    def get_data(
        self, explainer_identifier: ExplainerIdentifier
    ) -> list[FeatureDescription]:
        return self._feature_description_service.get_data(explainer_identifier)
