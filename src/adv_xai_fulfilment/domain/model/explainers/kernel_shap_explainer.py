from alibi.explainers import KernelShap

from ..data_type import DataType
from .explainer import Explainer
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer


class KernelSHAPExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="KernelSHAP",
            type=["BlackBox"],
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
        self.build_result = KernelShap(model.handler.predict, data.x)

