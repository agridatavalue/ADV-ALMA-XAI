from alibi.explainers import AnchorText, AnchorImage, AnchorTabular

from ..model import Model
from ..data_type import DataType
from .explainer import Explainer
from ..model_metadata import ModelMetaData
from .datatype_model_explainer import DataTypeModelExplainer


class AnchorsExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="Anchors",
            type=["BlackBox"],
            categories=["Classification"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TEXT, AnchorText),
                DataTypeModelExplainer(DataType.IMAGE, AnchorImage),
                DataTypeModelExplainer(DataType.TABULAR, AnchorTabular),
            ],
        )

    def can_match_with(self, model: Model, meta_data: ModelMetaData) -> bool:
        return False
