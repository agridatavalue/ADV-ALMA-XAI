from alibi.explainers import PartialDependence

from .Model import Model
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class PartialDependenceModel(Model):

    def __init__(self):
        super().__init__(
            name="PartialDependence",
            type=["BlackBox", "WhiteBox"],
            category=["Classification"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, PartialDependence)
            ],
        )
