from alibi.explainers import IntegratedGradients

from .explainer import Explainer
from ..data_type import DataType
from .datatype_model_explainer import DataTypeModelExplainer


class IntegratedGradientsExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="IntegratedGradients",
            type=["BlackBox"],
            categories=["Classification", "Regression"],
            explanations="local",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TEXT, IntegratedGradients),
                DataTypeModelExplainer(DataType.IMAGE, IntegratedGradients),
                DataTypeModelExplainer(DataType.TABULAR, IntegratedGradients),
            ],
        )

    def can_match_with(self, context: "ModelContext") -> bool:
        return False
