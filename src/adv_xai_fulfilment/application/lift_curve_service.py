import numpy as np

from .abstract_model_service import AbstractModelService
from ..domain.model.explainers.response_data import LiftCurve
from ..domain.model.explainer_identifier import ExplainerIdentifier


class LiftCurveService(AbstractModelService):

    def get_data(self, expl_id: ExplainerIdentifier) -> LiftCurve:
        context = self.get_context(expl_id)
        data = context.model_data
        
        if context.model_metadata.is_regression:
            raise ValueError("Lift curve is not applicable for regression models.")

        y_pred_prob = context.model.predict_proba(data.x_predict)
        if y_pred_prob.ndim == 2:
            y_pred_prob = y_pred_prob[:, 1]

        sorted_indices = np.argsort(y_pred_prob)[::-1]
        sorted_y_test = np.array(data.y_predict)[sorted_indices]

        cumulative_positives_model = np.cumsum(sorted_y_test)

        y_values = np.array(data.y_predict).flatten()  # Ensure y is 1D
        total_positives = np.sum(y_values)
        cumulative_positives_random = np.arange(1, len(y_values) + 1) * (total_positives / len(y_values))

        return (
            LiftCurve()
            .set_lift_curve_data(np.arange(1, len(data.y_predict) + 1))
            .set_cumulative_positives_model(cumulative_positives_model)
            .set_cumulative_positives_random(cumulative_positives_random)
        )