from logger import get_logger
from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import ConfusionMatrix


logger = get_logger()

class ConfusionMatrixService(AbstractModelService):

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> ConfusionMatrix:
        context = self.get_context(explainer_identifier)

        return context.model.get_confusion_matrix(context.model_data)
