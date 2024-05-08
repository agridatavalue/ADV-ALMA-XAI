from alibi.explainers import ALE

from .Model import Model
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class AleModel(Model):

    def __init__(self):
        super().__init__(
            name="ALE",
            type=["BlackBox"],
            category=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=False,
            data_type_explainers=[DataTypeModelExplainer(DataTypeModel.TABULAR, ALE)],
        )
