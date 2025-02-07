from ..domain.model import ExplainerIdentifier
from ..domain.model.explainers.responseData import FeatureImportance
from ..domain.service.FeatureImportanceServiceComponent import (
    FeatureImportanceServiceComponent,
)


class FeatureImportanceService:
    _feature_importance_service_comp: FeatureImportanceServiceComponent

    def __init__(self):
        self._feature_importance_service_comp = FeatureImportanceServiceComponent()

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> FeatureImportance:
        explainer_identifier.category = "regression"
        return self._feature_importance_service_comp.get_data(explainer_identifier)
