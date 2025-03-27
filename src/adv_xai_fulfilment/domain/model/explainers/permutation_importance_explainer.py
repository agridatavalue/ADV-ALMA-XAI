from alibi.explainers import PermutationImportance

from ..data_type import DataType
from .explainer import Explainer
from ....infrastructure.constants import Errors
from .datatype_model_explainer import DataTypeModelExplainer


class PermutationImportanceExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="PermutationImportance",
            type=["BlackBox"],
            categories=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, PermutationImportance)
            ],
        )

    def build(self, model, data:dict):
        assert isinstance(data, dict), Errors.DATA_NOT_DICT
        self.build_result = PermutationImportance(model.handler.predict, data)
