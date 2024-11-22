from alibi.explainers import KernelShap

from ..Model import Model
from ..DataType import DataType
from .Explainer import Explainer
from .DataTypeModelExplainer import DataTypeModelExplainer


class KernelSHAPExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="KernelSHAP",
            type=["BlackBox"],
            category=["Classification", "Regression"],
            explanations="both",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, KernelShap),
            ],
        )

    def can_match_with(self, model: Model, meta_data: dict) -> bool:
        return False
