import numpy as np
from shap import KernelExplainer

from .explainer import Explainer
from ..data_type import DataType
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer


class KernelExplainerExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="KernelExplainer",
            type=["BlackBox", "WhiteBox"],
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

    def build(self, model, data: ModelData):
        self.build_result = KernelExplainer(
            model.handler.predict if hasattr(model.handler, 'predict') else model.predict, 
            data.x_predict,
            feature_names=self.meta_data.feature_names if self.meta_data else None,
        )
        