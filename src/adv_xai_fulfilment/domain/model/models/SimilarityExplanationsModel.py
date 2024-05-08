from alibi.explainers import GradientSimilarity

from .Model import Model
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class SimilarityExplanationsModel(Model):

    def __init__(self):
        super().__init__(
            name="SimilarityExplanationsModel",
            type=["WhiteBox"],
            category=["Classification"],
            explanations="local",
            is_distributed=False,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TEXT, GradientSimilarity),
                DataTypeModelExplainer(DataTypeModel.IMAGE, GradientSimilarity),
                DataTypeModelExplainer(DataTypeModel.TABULAR, GradientSimilarity),
            ],
        )
