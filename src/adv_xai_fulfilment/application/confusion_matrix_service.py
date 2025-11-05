from logger import get_logger
from sklearn.metrics import confusion_matrix
from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import ConfusionMatrix

logger = get_logger()

class ConfusionMatrixService(AbstractModelService):

    def get_data(self, explainer_identifier: ExplainerIdentifier) -> ConfusionMatrix:
        context = self.get_context(explainer_identifier)

        obj = ConfusionMatrix()
        if context.model_metadata.is_ts_anomaly_detection:
            if len(context.model_metadata.target_names) > 0:
                preds = (context.model_data.y_predict == -1).astype(int)
                obj.data = confusion_matrix(context.model_data.y_test, preds)
            return obj
        
        obj.data = confusion_matrix(context.model_data.y_test, context.model_data.y_predict)
        return obj
