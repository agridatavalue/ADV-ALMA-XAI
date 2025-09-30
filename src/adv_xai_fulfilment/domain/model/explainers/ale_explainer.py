from alibi.explainers import ALE

from ..model import Model
from ..data_type import DataType
from .explainer import Explainer
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer
from src.adv_xai_fulfilment.infrastructure.constants import Errors


class AleExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="ALE",
            type=["BlackBox"],
            categories=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=False,
            data_type_explainers=[DataTypeModelExplainer(DataType.TABULAR, ALE)],
        )

    def build(self, model: Model, data: ModelData):
        if not self.meta_data:
            raise Errors.METADATA_NOT_INSTANCE_OF_MODEL_METADATA

        self.build_result = ALE(
            model.predict,
            feature_names=self.meta_data.feature_names,
            target_names=self.meta_data.target_names,
        )
