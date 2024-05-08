from alibi.explainers import CounterfactualRL

from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class CounterFactualsWithRlExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="TreeSHAPpathdependent",
            type=["BlackBox", "WhiteBox"],
            category=["Classification"],
            explanations="local",
            is_distributed=False,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.IMAGE, CounterfactualRL),
                DataTypeModelExplainer(DataTypeModel.TABULAR, CounterfactualRL),
            ],
        )
