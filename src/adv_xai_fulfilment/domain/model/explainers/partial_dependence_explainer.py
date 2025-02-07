from alibi.explainers import PartialDependence

from ..model import Model
from ..data_type import DataType
from .explainer import Explainer
from ..model_metadata import ModelMetaData
from .datatype_model_explainer import DataTypeModelExplainer


class PartialDependenceExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="PartialDependence",
            type=["BlackBox", "WhiteBox"],
            categories=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, PartialDependence)
            ],
        )

    def can_match_with(self, model: Model, meta_data: ModelMetaData) -> bool:
        return False
