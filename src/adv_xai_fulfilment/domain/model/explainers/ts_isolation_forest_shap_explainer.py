import shap
import numpy as np

from logger import get_logger
from .explainer import Explainer
from ..data_type import DataType
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer

logger = get_logger()

class TsIsolationForestShapExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="TsIsolationForestShap",
            type=["Unsupervised"],
            categories=["AnomalyDetection"],
            explanations="",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, shap.Explainer),
            ],
        )

    def build(self, model, data: ModelData):
        masker = shap.maskers.Independent(data.x_train, max_samples=100) 
        self.build_result = shap.Explainer(
            model.handler.decision_function, 
            masker=masker,
            feature_names=self.meta_data.feature_names if self.meta_data else None, 
        )

    def get_shap_values(self, x_test: np.ndarray) -> np.ndarray:
        if self.build_result is None:
            raise RuntimeError("Explainer non ancora buildato e fittato")
        result = self.build_result(x_test)
        return result.values if hasattr(result, "values") else np.array(result)
