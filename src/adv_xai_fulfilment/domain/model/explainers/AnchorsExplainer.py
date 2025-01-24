from alibi.explainers import AnchorText, AnchorImage, AnchorTabular

from ..Model import Model
from ..DataType import DataType
from .Explainer import Explainer
from ..ModelMetaData import ModelMetaData
from .DataTypeModelExplainer import DataTypeModelExplainer


class AnchorsExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="Anchors",
            type=["BlackBox"],
            category=["Classification"],
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
