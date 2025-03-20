import pandas as pd
from sklearn.inspection import partial_dependence

from ...explainers.response_data import IndividualConditionalExpectations

class IndividualConditionalExpectationsExecutor:
    def process(self, model, X: pd.DataFrame, feature: str) -> IndividualConditionalExpectations:
        pd_results = partial_dependence(
            model.handler, 
            X, 
            [feature], 
            kind="both"
        )

        return IndividualConditionalExpectations(
            grid_values=pd_results["values"][0],
            pdp_mean=pd_results["average"][0],
            ice_curves=pd_results["individual"][0]
        )
