import numpy as np

from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier

class PlotScatterObservedPredictedService(AbstractModelService):

    def genarate_data_for_partner(
        self, explainer_identifier: ExplainerIdentifier
    ) -> dict["y_observed" : np.ndarray, "y_predicted" : np.ndarray]:
        context = self.get_context(explainer_identifier)
        
        X_test = np.array(context.model_data.x_predict)
        y_test = np.array(context.model_data.y_predict)

        return {"y_observed": y_test, "y_predicted": context.model.handler.predict(X_test)}
