from alibi.explainers import KernelShap

from .Model import Model
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class KernelSHAPModel(Model):

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
