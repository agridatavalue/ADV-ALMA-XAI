from alibi.explainers import ALE

from ..Model import Model
from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer
from src.adv_xai_fulfilment.infrastructure.Constants import Errors


class AleExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="ALE",
            type=["BlackBox"],
            category=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=False,
            data_type_explainers=[DataTypeModelExplainer(DataTypeModel.TABULAR, ALE)],
        )

    def build(self, model: Model, data: dict):
        assert isinstance(self.meta_data, dict), Errors.METADATA_NOT_DICT
        self.build_result = ALE(
            model.handler.predict,
            feature_names=self.meta_data.get("featurenames"),
            target_names=self.meta_data.get("targetnames"),
        )
