from alibi.explainers import PartialDependenceVariance

from .Model import Model
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class PartialDependenceVarianceModel(Model):

    def __init__(self):
        super().__init__(
            name="PartialDependenceVariance",
            type=["BlackBox", "WhiteBox"],
            category=["Classification"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, PartialDependenceVariance)
            ],
        )
