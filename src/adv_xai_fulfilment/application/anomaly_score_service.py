import numpy as np

from logger import get_logger
from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import AnomalyScore, AnomalyVsNormal

logger = get_logger()

class AnomalyScoreService(AbstractModelService):

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> AnomalyScore:
        context = self.get_context(explainer_identifier)

        scores = context.model.handler.decision_function(context.model_data.x_predict)
        return AnomalyScore.from_data(context.model_data.data_train).assign_scores(scores)
    
    def get_anomaly_vs_normal_data(self, explainer_identifier: ExplainerIdentifier) -> AnomalyVsNormal:
        context = self.get_context(explainer_identifier)
        
        iso_preds = context.model.handler.predict(context.model_data.x_predict)

        so_preds: np.ndarray = (iso_preds == -1).astype(int)  # Convert -1 (anomaly) to 1, and 1 (normal) to 0

        return AnomalyVsNormal().set_data(so_preds.tolist())

