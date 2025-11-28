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

        # Use test labels and predictions directly from ModelData
        y_test = np.array(data.y_test).flatten()
        y_pred = np.array(data.y_predict).flatten()

        # If predictions are class labels, try to get probabilities instead
        if len(np.unique(y_pred)) == 2 and set(np.unique(y_pred)) == {0, 1}:
            # Looks like class labels, not probabilities
            if hasattr(context.model.handler, "predict_proba"):
                # Compute probabilities for the test set, not the full data
                y_pred = context.model.handler.predict_proba(data.x_predict)[:, 1]
            else:
                raise ValueError("Model does not provide predict_proba(), cannot compute lift curve properly.")

        y_pred = np.array(y_pred).flatten()

        # Allinei le lunghezze per evitare out-of-bounds
        min_len = min(len(y_test), len(y_pred))
        if min_len == 0:
            raise ValueError("Cannot compute lift curve: zero-length arrays.")

        if len(y_test) != len(y_pred):
            y_test = y_test[:min_len]
            y_pred = y_pred[:min_len]

        # Sort by predicted probability
        sorted_indices = np.argsort(y_pred)[::-1]
        sorted_y_test = y_test[sorted_indices]

        # Compute cumulative positives (model)
        cumulative_positives_model = np.cumsum(sorted_y_test)

        # Compute cumulative positives (random baseline)
        n = len(sorted_y_test)
        total_positives = np.sum(sorted_y_test)
        cumulative_positives_random = np.arange(1, n + 1) * (total_positives / n)

        return (
            LiftCurve()
            .set_lift_curve_data(np.arange(1, n + 1))
            .set_cumulative_positives_model(cumulative_positives_model)
            .set_cumulative_positives_random(cumulative_positives_random)
        )
