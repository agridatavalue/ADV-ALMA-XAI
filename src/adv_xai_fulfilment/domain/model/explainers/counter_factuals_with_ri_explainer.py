from alibi.explainers import CounterfactualRL

from ..data_type import DataType
from .explainer import Explainer
from .datatype_model_explainer import DataTypeModelExplainer


class CounterFactualsWithRlExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="TreeSHAPpathdependent",
            type=["BlackBox", "WhiteBox"],
            categories=["Classification"],
            explanations="local",
            is_distributed=False,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.IMAGE, CounterfactualRL),
                DataTypeModelExplainer(DataType.TABULAR, CounterfactualRL),
            ],
        )

    def can_match_with(self, context: "ModelContext") -> bool:
        return False
