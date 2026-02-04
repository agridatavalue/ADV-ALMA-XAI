import numpy as np
import pandas as pd
from shap import KernelExplainer

from .explainer import Explainer
from ..data_type import DataType
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer
from src.adv_xai_fulfilment.infrastructure.helper import Helper


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
        if len(x_test) > Helper.get_limit_for_data_samples():
            if isinstance(x_test, pd.DataFrame):
                x_test = x_test.sample(Helper.get_limit_for_data_samples(), random_state=42)
            
        return self.build_result.shap_values(x_test)

    def build(self, model, data: ModelData):
        self.build_result = KernelExplainer(
            model.handler.predict if hasattr(model.handler, 'predict') else model.predict, 
            data.x_predict,
            feature_names=self.meta_data.feature_names if self.meta_data else None,
        )
        