import numpy as np
from alibi.explainers import KernelShap

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

    def get_shap_values(self, x_test: np.array):
        explanation = self.build_result.explain(x_test)
        return explanation.shap_values
