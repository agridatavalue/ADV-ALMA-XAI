from alibi.explainers import GradientSimilarity

from ..Model import Model
from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class SimilarityExplanationsExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="SimilarityExplanations",
            type=["WhiteBox"],
            category=["Classification", "Regression"],
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

    def can_match_with(self, model: Model, meta_data: dict) -> bool:
        return False
