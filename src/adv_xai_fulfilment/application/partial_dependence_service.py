import numpy as np

from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import PartialDependence
from ..domain.model.explainers.partial_dependence_explainer import PartialDependenceExplainer

class PartialDependenceService(AbstractModelService):

    def get_data(self, request: ExplainerIdentifier, feature: str) -> PartialDependence:
        context = self.get_context(request)
        
        feature_idx = feature
        if isinstance(feature, str):
            feature_idx = list(context.model_data.x_train.columns).index(feature)

        explainer = self._get_explanator(request, PartialDependenceExplainer())
        
        explanation = explainer.explain(
            X=context.model_data.x_train.values,
            features=[feature_idx],
            grid_resolution=50  # Match sklearn's resolution
        )
        
        pdp_values = np.asarray(explanation.pd_values[0]).flatten().tolist()
        
        return PartialDependence(
            feature_values=np.asarray(explanation.feature_values[0]).flatten().tolist(),
            std_effect=float(np.std(pdp_values)),
            pdp_values=pdp_values,
            mean_effect=float(np.mean(pdp_values)),
        )