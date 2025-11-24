from alibi.explainers import CEM

from ..model import Model
from .explainer import Explainer
from ..data_type import DataType
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer
from src.adv_xai_fulfilment.infrastructure.constants import Errors


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

    def build(self, model: Model, data: ModelData):
        if not self.meta_data:
            raise Errors.METADATA_NOT_INSTANCE_OF_MODEL_METADATA

        self.build_result = CEM(
            model.predict,
            feature_names=self.meta_data.feature_names,
            target_names=self.meta_data.target_names,
        )

    def can_match_with(self, context: "ModelContext") -> bool:
        return False
