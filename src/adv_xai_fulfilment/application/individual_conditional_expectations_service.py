import numpy as np
from logger import get_logger

from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import IndividualConditionalExpectations
from ..domain.model.explainers.alibi_partial_dependence_explainer import AlibiPartialDependenceExplainer
from ..domain.model.explainers.sklearn_partial_dependence_explainer import SkLearnPartialDependenceExplainer

logger = get_logger()


class IndividualConditionalExpectationService(AbstractModelService):

    def get_data(self, request: ExplainerIdentifier, feature: str) -> IndividualConditionalExpectations:
        context = self.get_context(request)

        feature_idx = feature
        if isinstance(feature, str):
            feature_idx = list(context.model_data.x_train.columns).index(feature)

        logger.debug(f"Using feature index: {feature_idx} for feature: {feature}")
        
        for expl_to_download in [SkLearnPartialDependenceExplainer(), AlibiPartialDependenceExplainer()]:
            try:
                explainer = self._get_explanator(request, expl_to_download)
                if isinstance(expl_to_download, SkLearnPartialDependenceExplainer):
                    raw = explainer[feature]["individual"][0]
                    ice = np.array(raw)
                    ice = ice[:, :, None]
                    return IndividualConditionalExpectations(
                        pdp_mean=explainer[feature]["average"][0],
                        ice_curves=ice,
                        grid_values=explainer[feature]["values"][0],
                    )
                elif isinstance(expl_to_download, AlibiPartialDependenceExplainer):
                    explanation = explainer.explain(
                        X=context.model_data.x_train.values,
                        features=[feature_idx],
                        grid_resolution=50,  # Match sklearn's resolution
                        kind="both"
                    )
                    raw_ice = np.asarray(explanation.data['ice_values'][0]).T  # (samples, grid)
                    ice = raw_ice[:, :, None]
                    return IndividualConditionalExpectations(
                        pdp_mean=np.asarray(explanation.data['pd_values'][0]).flatten(),
                        ice_curves=raw_ice.T,
                        grid_values=np.asarray(explanation.data['feature_values'][0]),
                    )
            except ValueError as e:
                logger.warning("Warning", e)
                continue

            raise ValueError("Cannot calculate ice")
