from alibi.explainers import ALE

from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class AleExplainer(Explainer):

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
