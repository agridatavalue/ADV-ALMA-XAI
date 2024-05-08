from alibi.explainers import RegressionExplainer

from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class RegressionExplainerExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="RegressionExplainerModel",
            type=["BlackBox"],
            category=["Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=False,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, RegressionExplainer)
            ],
        )
