import numpy as np
from logger import get_logger

from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import PartialDependence
from ..domain.model.machine_learning_model.scikitlearn_model import ScikitLearnModel
from ..domain.model.explainers.alibi_partial_dependence_explainer import AlibiPartialDependenceExplainer
from ..domain.model.explainers.sklearn_partial_dependence_explainer import SkLearnPartialDependenceExplainer

logger = get_logger()

class PartialDependenceService(AbstractModelService):

    def get_data(self, request: ExplainerIdentifier, feature: str) -> PartialDependence:
        context = self.get_context(request)

        feature_idx = feature
        if isinstance(feature, str):
            feature_idx = list(context.model_data.x_train.columns).index(feature)

        logger.debug(f"Using feature index: {feature_idx} for feature: {feature}")
        
        for expl_to_download in [SkLearnPartialDependenceExplainer(), AlibiPartialDependenceExplainer()]:
            try:
                explainer = self._get_explanator(request, expl_to_download)
                if isinstance(expl_to_download, SkLearnPartialDependenceExplainer):
                    pdp_values = np.asarray(explainer[feature]["average"][0]).flatten().tolist()
                    return PartialDependence(
                        pdp_values=pdp_values,
                        mean_effect=float(np.mean(pdp_values)),
                        std_effect=float(np.std(pdp_values)),
                        feature_values=np.asarray(explainer[feature]["values"][0]).flatten().tolist(),
                    )
                elif isinstance(expl_to_download, AlibiPartialDependenceExplainer):
                    explanation = explainer.explain(
                        X=context.model_data.x_train.values,
                        features=[feature_idx],
                        grid_resolution=50,  # Match sklearn's resolution
                        kind="both"
                    )
                    pdp_values = np.asarray(explanation.pd_values[0]).flatten().tolist()
                    return PartialDependence(
                        feature_values=np.asarray(explanation.feature_values[0]).flatten().tolist(),
                        std_effect=float(np.std(pdp_values)),
                        pdp_values=pdp_values,
                        mean_effect=float(np.mean(pdp_values)),
                    )
            except ValueError as e:
                print("Warning", e)
                continue

            raise ValueError("Cannot calculate ice")
