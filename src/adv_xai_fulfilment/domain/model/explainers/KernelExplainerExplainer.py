import numpy as np
from shap import KernelExplainer

from ..DataType import DataType
from .Explainer import Explainer
from .DataTypeModelExplainer import DataTypeModelExplainer
from src.adv_xai_fulfilment.infrastructure.Constants import Errors


class KernelExplainerExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="KernelExplainer",
            type=["BlackBox"],
            categories=["Classification", "Regression"],
            explanations="both",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, KernelExplainer),
            ],
        )

    def get_shap_values(self, x_test: np.array) -> np.array:
        return self.build_result.shap_values(x_test)

    def build(self, model, data: dict):
        assert isinstance(data, dict), Errors.DATA_NOT_DICT
        self.build_result = KernelExplainer(model.handler.predict, data.get("x"))
