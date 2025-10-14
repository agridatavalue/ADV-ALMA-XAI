from alibi.explainers import GradientSimilarity

from ..data_type import DataType
from .explainer import Explainer
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer


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

    def build(self, model, data: ModelData):
        self.build_result = GradientSimilarity(model.predict)


