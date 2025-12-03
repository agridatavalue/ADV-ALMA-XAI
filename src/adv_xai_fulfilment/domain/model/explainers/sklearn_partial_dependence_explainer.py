from sklearn.inspection import partial_dependence

from .explainer import Explainer
from ..data_type import DataType
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer
from ..machine_learning_model.scikitlearn_model import ScikitLearnModel


class SkLearnPartialDependenceExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="SkLearnPartialDependence",
            type=["BlackBox", "WhiteBox"],
            categories=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, partial_dependence)
            ],
        )
        
    def can_match_with(self, context: "ModelContext") -> bool:
        return super().can_match_with(context) and isinstance(context.model, ScikitLearnModel)

    def build(self, model, data: ModelData):
        build: dict = {}
        for feature_index in range(len(self.meta_data.feature_names if self.meta_data else [])):
            build[self.meta_data.feature_names[feature_index]] = partial_dependence(
                X=data.x_train,
                features=[feature_index],
                estimator=model.handler,
                feature_names=self.meta_data.feature_names if self.meta_data else None,
                kind="both"
            )
        self.build_result = build
