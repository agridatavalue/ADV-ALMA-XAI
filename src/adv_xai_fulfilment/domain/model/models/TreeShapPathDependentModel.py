from alibi.explainers import TreeShap

from .Model import Model
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class TreeShapPathDependentModel(Model):

    def __init__(self):
        super().__init__(
            name="TreeSHAPpathdependent",
            type=["WhiteBox"],
            category=["Classification"],
            explanations="both",
            is_distributed=False,
            train_set_required=None,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, TreeShap)
            ],
        )
