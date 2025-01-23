import numpy as np

from .ExplainerResponseData import ExplainerResponseData


class PartialDependence(ExplainerResponseData):
    std_effect: float
    mean_effect: float
    pdp_values: np.ndarray
    lower_bound: np.ndarray
    upper_bound: np.ndarray
    feature_values: np.ndarray

    def __init__(
        self,
        *,
        feature_values: np.ndarray,
        pdp_values: np.ndarray,
        mean_effect: float,
        std_effect: float,
        lower_bound: np.ndarray = None,
        upper_bound: np.ndarray = None,
    ):
        self.pdp_values = pdp_values
        self.std_effect = std_effect
        self.mean_effect = mean_effect
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.feature_values = feature_values

    def to_dict(self) -> dict:
        return {
            "std_effect": float(self.std_effect),
            "mean_effect": float(self.mean_effect),
            "pdp_values": self.pdp_values.tolist(),
            "lower_bound": (
                self.lower_bound.tolist() if self.lower_bound is not None else None
            ),
            "upper_bound": (
                self.upper_bound.tolist() if self.upper_bound is not None else None
            ),
            "feature_values": self.feature_values.tolist(),
        }

    def __repr__(self) -> str:
        return f"PartialDependence(std_effect={self.std_effect}, mean_effect={self.mean_effect}, pdp_values={self.pdp_values.tolist()}, lower_bound={self.lower_bound.tolist() if self.lower_bound is not None else None}, upper_bound={self.upper_bound.tolist() if self.upper_bound is not None else None}, feature_values={self.feature_values.tolist()})"
