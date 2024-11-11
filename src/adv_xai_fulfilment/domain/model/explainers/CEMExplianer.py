from alibi.explainers import CEM

from ..Model import Model
from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class ContrastiveExplanationMethodExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="CEM",
            type=["BlackBox"],
            category=["Classification"],
            explanations="local",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[DataTypeModelExplainer(DataTypeModel.TABULAR, CEM), DataTypeModelExplainer(DataTypeModel.IMAGE,CEM)],
        )

    def build(self, model: Model, data: dict):
        self.build_result = CEM(
            model.handler.predict,
            feature_names=self.meta_data.get("featurenames"),
            target_names=self.meta_data.get("targetnames"),
        )

    def can_match_with(self, model: Model, meta_data: dict) -> bool:
        return False
