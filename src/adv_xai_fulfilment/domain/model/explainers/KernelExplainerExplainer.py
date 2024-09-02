import numpy as np
from shap import KernelExplainer

from ..Model import Model
from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class KernelExplainerExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="KernelExplainer",
            type=["BlackBox"],
            category=["Classification", "Regression"],
            explanations="both",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, KernelExplainer),
            ],
        )

    def get_shap_values(
        self, model: Model, x_train: np.array, x_test: np.array
    ) -> np.array:
        explainer = KernelExplainer(model.handler.predict, x_train)
        return explainer.shap_values(x_test)
