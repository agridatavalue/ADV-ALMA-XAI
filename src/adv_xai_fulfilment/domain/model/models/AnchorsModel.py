from alibi.explainers import AnchorText, AnchorImage, AnchorTabular

from .Model import Model
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class AnchorsModel(Model):

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
                DataTypeModelExplainer(DataTypeModel.TEXT, AnchorText),
                DataTypeModelExplainer(DataTypeModel.IMAGE, AnchorImage),
                DataTypeModelExplainer(DataTypeModel.TABULAR, AnchorTabular),
            ],
        )
