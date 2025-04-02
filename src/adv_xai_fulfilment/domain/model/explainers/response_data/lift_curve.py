import pandas as pd

from .explainer_response_data import ExplainerResponseData

class LiftCurve(ExplainerResponseData):
    _lift_curve_data: pd.Series
    _cumulative_positives_model: pd.Series
    _cumulative_positives_random: pd.Series

    def __init__(self):
        super().__init__(endpoint='lift_curve')

    def set_lift_curve_data(self, lift_curve_data: pd.Series) -> "LiftCurve":
        self._lift_curve_data = lift_curve_data
        return self

    def set_cumulative_positives_model(self, cumulative_positives_model: pd.Series) -> "LiftCurve":
        self._cumulative_positives_model = cumulative_positives_model
        return self

    def set_cumulative_positives_random(self, cumulative_positives_random: pd.Series) -> "LiftCurve":
        self._cumulative_positives_random = cumulative_positives_random
        return self
    
    def to_dict(self) -> dict:
        return {
            "lift_curve_data": self._lift_curve_data.tolist(),
            "cumulative_positives_model": self._cumulative_positives_model.tolist(),
            "cumulative_positives_random": self._cumulative_positives_random.tolist(),
        }