from shap import DeepExplainer

from ..DataType import DataType
from .Explainer import Explainer
from .DataTypeModelExplainer import DataTypeModelExplainer


class DeepExplainerExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="DeepExplainer",
            type=["BlackBox"],
            category=["Classification", "Regression"],
            explanations="both",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, DeepExplainer),
                DataTypeModelExplainer(DataType.IMAGE, DeepExplainer),
            ],
        )

    def get_shap_values(self, x_test):
        return self.build_result.shap_values(x_test)
