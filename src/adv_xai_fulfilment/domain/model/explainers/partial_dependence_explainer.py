from alibi.explainers import PartialDependence

from ..data_type import DataType
from .explainer import Explainer
from ....infrastructure.constants import Errors
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

    def build(self, model, data: dict):
        assert isinstance(data, dict), Errors.DATA_NOT_DICT
        self.build_result = PartialDependence(model.handler.predict, data)
