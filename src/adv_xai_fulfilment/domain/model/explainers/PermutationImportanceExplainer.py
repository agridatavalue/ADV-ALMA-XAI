from alibi.explainers import PermutationImportance

from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class PermutationImportanceExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="PermutationImportance",
            type=["BlackBox"],
            category=["Classification"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, PermutationImportance)
            ],
        )
