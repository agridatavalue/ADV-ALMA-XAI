from alibi.explainers import KernelShap

from ..model import Model
from ..data_type import DataType
from .explainer import Explainer
from .datatype_model_explainer import DataTypeModelExplainer


class KernelSHAPExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="KernelSHAP",
            type=["BlackBox"],
            categories=["Classification", "Regression"],
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
