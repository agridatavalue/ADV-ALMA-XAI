from alibi.explainers import GradientSimilarity

from ..Model import Model
from ..DataType import DataType
from .Explainer import Explainer
from ..ModelMetaData import ModelMetaData
from .DataTypeModelExplainer import DataTypeModelExplainer


class SimilarityExplanationsExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="SimilarityExplanations",
            type=["WhiteBox"],
            categories=["Classification", "Regression"],
            explanations="local",
            is_distributed=False,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TEXT, GradientSimilarity),
                DataTypeModelExplainer(DataType.IMAGE, GradientSimilarity),
                DataTypeModelExplainer(DataType.TABULAR, GradientSimilarity),
            ],
        )

    def can_match_with(self, model: Model, meta_data: ModelMetaData) -> bool:
        return False
