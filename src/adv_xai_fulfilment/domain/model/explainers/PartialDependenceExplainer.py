from alibi.explainers import PartialDependence

from src.adv_xai_fulfilment.domain.model.Model import Model

from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class PartialDependenceExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="PartialDependence",
            type=["BlackBox", "WhiteBox"],
            category=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, PartialDependence)
            ],
        )

    def can_match_with(self, model: Model, meta_data: dict) -> bool:
        return False
