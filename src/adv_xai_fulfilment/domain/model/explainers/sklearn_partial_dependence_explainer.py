import numpy as np
import pandas as pd
from sklearn.inspection import partial_dependence


from logger import get_logger
from .explainer import Explainer
from ..data_type import DataType
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer
from ..machine_learning_model.scikitlearn_model import ScikitLearnModel

logger = get_logger()


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
        
        for i, feature_name in enumerate(self.meta_data.feature_names if self.meta_data else []):
            if isinstance(data.x_train, pd.DataFrame):
                values = data.x_train[feature_name]
                feature_ref = feature_name
            else:
                values = data.x_train[:, i]
                feature_ref = i

            if pd.Series(values).nunique(dropna=True) < 2:
                logger.warning(f"Skipping {feature_name}: not enough unique values")
                continue

            try:
                build[feature_name] = partial_dependence(
                    X=data.x_train,
                    features=[feature_ref],
                    estimator=model.handler,
                    feature_names=self.meta_data.feature_names,
                    kind="both"
                )
            except Exception as e:
                logger.warning(f"Skipping {feature_name}: {e}")
        
        self.build_result = build
