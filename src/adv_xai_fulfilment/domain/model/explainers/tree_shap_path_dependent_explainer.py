from alibi.explainers import TreeShap

from .explainer import Explainer
from ..data_type import DataType
from .datatype_model_explainer import DataTypeModelExplainer


class TreeShapPathDependentExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="TreeSHAPpathdependent",
            type=["WhiteBox"],
            categories=["Classification", "Regression"],
            explanations="both",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[DataTypeModelExplainer(DataType.TABULAR, TreeShap)],
        )

    def can_match_with(self, context: "ModelContext") -> bool:
        return False
