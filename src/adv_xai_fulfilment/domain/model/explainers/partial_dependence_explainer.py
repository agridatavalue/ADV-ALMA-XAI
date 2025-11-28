from alibi.explainers import PartialDependence

from .explainer import Explainer
from ..data_type import DataType
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer


class PartialDependenceExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="PartialDependence",
            type=["BlackBox", "WhiteBox"],
            categories=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, PartialDependence)
            ],
        )

    def build(self, model, data: ModelData):
        self.build_result = PartialDependence(
            predictor=model.predict_proba if self.meta_data and self.meta_data.is_classification else model.predict,
            feature_names=self.meta_data.feature_names if self.meta_data else None,
            target_names=self.meta_data.target_names if self.meta_data else None,
        )
