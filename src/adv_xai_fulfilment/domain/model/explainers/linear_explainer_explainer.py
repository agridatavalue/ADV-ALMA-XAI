import torch
from shap import LinearExplainer

from src.adv_xai_fulfilment.infrastructure.helper import Helper
from src.adv_xai_fulfilment.domain.model.model_data import ModelData

from .explainer import Explainer
from ..data_type import DataType
from .datatype_model_explainer import DataTypeModelExplainer


class LinearExplainerExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="LinearExplainer",
            type=["WhiteBox"],
            categories=["Classification", "Regression"],
            explanations="both",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, LinearExplainer),
            ],
        )
        
    def can_match_with(self, context: "ModelContext") -> bool:
        return (
            super().can_match_with(context) 
            and len(context.model_data.data_train) > Helper.get_limit_for_data_samples()
        )

    def get_shap_values(self, x_test):
        return self.build_result.shap_values(x_test)
    
    def build(self, model, data: ModelData):
        data_to_explain = data.x_predict
        if model.can_handle_federated():
            data_to_explain = torch.tensor(data.x_predict, dtype=torch.float32).transpose(1, 2)
        
        self.build_result = LinearExplainer(model.handler, data_to_explain)
