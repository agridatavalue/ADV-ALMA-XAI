from alibi.explainers import RegressionExplainer

from .Model import Model
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class RegressionExplainerModel(Model):

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
