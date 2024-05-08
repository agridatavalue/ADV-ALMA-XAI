from alibi.explainers import KernelShap

from src.adv_xai_fulfilment.domain.model.Model import Model

from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class KernelSHAPExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="KernelSHAP",
            type=["BlackBox"],
            category=["Classification"],
            explanations="both",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, KernelShap),
            ],
        )

    def canMatchWith(self, model: Model, meta_data: dict) -> bool:
        return super().canMatchWith(model, meta_data) and model.name == meta_data.get(
            "model"
        )
