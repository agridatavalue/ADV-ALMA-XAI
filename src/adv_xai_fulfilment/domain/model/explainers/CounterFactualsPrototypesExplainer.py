from alibi.explainers import CounterfactualRL

from ..Model import Model
from ..DataType import DataType
from .Explainer import Explainer
from ..ModelMetaData import ModelMetaData
from .DataTypeModelExplainer import DataTypeModelExplainer


class CounterFactualsPrototypesExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="TreeSHAPpathdependent",
            type=["BlackBox", "WhiteBox"],
            category=["Classification"],
            explanations="local",
            is_distributed=False,
            train_set_required=None,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.IMAGE, CounterfactualRL),
                DataTypeModelExplainer(DataType.TABULAR, CounterfactualRL),
            ],
        )

    def can_match_with(self, model: Model, meta_data: ModelMetaData) -> bool:
        return False
