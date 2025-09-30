import numpy as np
from alibi.explainers import KernelShap

from logger import get_logger
from ..data_type import DataType
from .explainer import Explainer
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer

logger = get_logger()

class KernelSHAPExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="KernelSHAP",
            type=["BlackBox", "WhiteBox"],
            categories=["Classification", "Regression"],
            explanations="both",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, KernelShap),
            ],
        )

    def build(self, model, data: ModelData):
        self.build_result = KernelShap(model.predict, data.x_train)
        self.build_result.fit(data.x_train)

        logger.info(f"Explainer fitted? {getattr(self.build_result, 'fitted', None)}")


    def get_shap_values(self, x_test: np.ndarray) -> np.ndarray:
        if self.build_result is None:
            raise RuntimeError("Explainer non ancora buildato e fittato")
        explanation = self.build_result.explain(x_test)
        return explanation.shap_values