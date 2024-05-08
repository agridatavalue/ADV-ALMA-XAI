from alibi.explainers import CounterfactualRL

from .Model import Model
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class CounterFactualsWithRlModel(Model):

    def __init__(self):
        super().__init__(
            name="TreeSHAPpathdependent",
            type=["BlackBox", "WhiteBox"],
            category=["Classification"],
            explanations="local",
            is_distributed=False,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.IMAGE, CounterfactualRL),
                DataTypeModelExplainer(DataTypeModel.TABULAR, CounterfactualRL),
            ],
        )
