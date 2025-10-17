import numpy as np

from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import IndividualConditionalExpectations
from ..domain.model.explainers.partial_dependence_explainer import PartialDependenceExplainer


class IndividualConditionalExpectationService(AbstractModelService):

    def get_data(self, request: ExplainerIdentifier, feature: str) -> IndividualConditionalExpectations:
        context = self.get_context(request)

        feature_idx = feature
        if isinstance(feature, str):
            feature_idx = list(context.model_data.x_train.columns).index(feature)

        print(f"Using feature index: {feature_idx} for feature: {feature}")

        explainer = self._get_explanator(request, PartialDependenceExplainer())

        # Generate the explanation
        explanation = explainer.explain(
            X=context.model_data.x_train.values,
            features=[feature_idx],
            grid_resolution=50,  # Match sklearn's resolution
            kind="both"
        )
        
        pdp_values = np.asarray(explanation.data['pd_values'][0]).flatten()
        ice_curves = np.asarray(explanation.data['ice_values'][0])  # shape: (n_samples, grid_resolution)
        grid_values = np.asarray(explanation.data['feature_values'][0])

        # Restituisce l'oggetto con tutti i valori ICE + PDP
        return IndividualConditionalExpectations(
            pdp_mean=pdp_values,
            ice_curves=ice_curves,
            grid_values=grid_values,
        )
