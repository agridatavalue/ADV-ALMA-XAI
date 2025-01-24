from alibi.explainers import PermutationImportance

from ..Model import Model
from ..DataType import DataType
from .Explainer import Explainer
from ..ModelMetaData import ModelMetaData
from .DataTypeModelExplainer import DataTypeModelExplainer


class PermutationImportanceExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="PermutationImportance",
            type=["BlackBox"],
            categories=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, PermutationImportance)
            ],
        )

    def can_match_with(self, model: Model, meta_data: ModelMetaData) -> bool:
        return False
