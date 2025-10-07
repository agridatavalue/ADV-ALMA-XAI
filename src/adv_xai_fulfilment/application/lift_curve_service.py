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
        y_test = np.array(data._y_test)
        y_pred = np.array(data._y_predict)

        # Ensure 1D
        y_test = y_test.flatten()
        y_pred = y_pred.flatten()
        
        # If predictions are class labels, try to get probabilities instead
        if len(np.unique(y_pred)) == 2 and set(np.unique(y_pred)) == {0, 1}:
            # Looks like class labels, not probabilities
            if hasattr(context.model.handler, "predict_proba"):
                # Compute probabilities for the test set, not the full data
                y_pred = context.model.handler.predict_proba(data._x_predict)[:, 1]
            else:
                raise ValueError("Model does not provide predict_proba(), cannot compute lift curve properly.")

        # Check shape alignment before proceeding
        if y_test.shape[0] != y_pred.shape[0]:
            raise ValueError(
                f"Shape mismatch: y_test has {y_test.shape[0]} elements, "
                f"but y_pred has {y_pred.shape[0]}."
            )

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
