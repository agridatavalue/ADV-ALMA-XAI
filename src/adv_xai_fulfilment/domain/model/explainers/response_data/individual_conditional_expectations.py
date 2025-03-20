import numpy as np

from .explainer_response_data import ExplainerResponseData

class IndividualConditionalExpectations(ExplainerResponseData):
    pdp_mean: np.ndarray
    ice_curves: np.ndarray
    grid_values: np.ndarray

    def __init__(self,
        *,
        pdp_mean: np.ndarray,
        ice_curves: np.ndarray,
        grid_values: np.ndarray,
    ):
        super().__init__('individual-conditional-expectations')
        self.pdp_mean = pdp_mean
        self.ice_curves = ice_curves
        self.grid_values = grid_values

    def to_dict(self) -> dict:
        return {
            "pdp_mean": self.pdp_mean.tolist(),
            "ice_curves": self.ice_curves.tolist(),
            "grid_values": self.grid_values.tolist(),
        }