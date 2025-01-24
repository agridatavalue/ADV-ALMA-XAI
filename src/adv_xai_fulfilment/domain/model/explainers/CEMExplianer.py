from alibi.explainers import CEM

from ..Model import Model
from ..DataType import DataType
from .Explainer import Explainer
from .DataTypeModelExplainer import DataTypeModelExplainer
from src.adv_xai_fulfilment.infrastructure.Constants import Errors


class ContrastiveExplanationMethodExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="CEM",
            type=["BlackBox"],
            categories=["Classification"],
            explanations="local",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, CEM),
                DataTypeModelExplainer(DataType.IMAGE, CEM),
            ],
        )

    def build(self, model: Model, data: dict):
        if not self.meta_data:
            raise Errors.METADATA_NOT_INSTANCE_OF_MODEL_METADATA

        self.build_result = CEM(
            model.handler.predict,
            feature_names=self.meta_data.feature_names,
            target_names=self.meta_data.target_names,
        )

    def can_match_with(self, model: Model, meta_data: dict) -> bool:
        return False
