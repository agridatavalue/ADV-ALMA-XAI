from shap import DeepExplainer

from src.adv_xai_fulfilment.domain.model.model_data import ModelData

from ..data_type import DataType
from .explainer import Explainer
from .datatype_model_explainer import DataTypeModelExplainer


class DeepExplainerExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="DeepExplainer",
            type=["BlackBox"],
            categories=["Classification", "Regression"],
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
    
    def build(self, model, data: ModelData):
        return DeepExplainer(model.handler, data.x_train)
