from alibi.explainers import PartialDependenceVariance

from ..Model import Model
from ..DataType import DataType
from .Explainer import Explainer
from ..ModelMetaData import ModelMetaData
from .DataTypeModelExplainer import DataTypeModelExplainer


class PartialDependenceVarianceExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="PartialDependenceVariance",
            type=["BlackBox", "WhiteBox"],
            category=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, PartialDependenceVariance)
            ],
        )

    def can_match_with(self, model: Model, meta_data: ModelMetaData) -> bool:
        return False
