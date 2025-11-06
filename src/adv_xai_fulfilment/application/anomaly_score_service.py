from logger import get_logger
from .abstract_model_service import AbstractModelService
from ..domain.model.explainers.response_data import AnomalyScore
from ..domain.model.explainer_identifier import ExplainerIdentifier

logger = get_logger()

class AnomalyScoreService(AbstractModelService):

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> AnomalyScore:
        context = self.get_context(explainer_identifier)

        scores = context.model.handler.decision_function(context.model_data.x_predict)
        return AnomalyScore.from_data(context.model_data.data_train).assign_scores(scores)
