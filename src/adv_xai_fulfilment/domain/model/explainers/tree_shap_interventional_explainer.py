import numpy as np
from alibi.explainers import TreeShap

from ..model import Model
from .explainer import Explainer
from ..data_type import DataType
from ..model_data import ModelData
from ....infrastructure.constants import Errors
from .datatype_model_explainer import DataTypeModelExplainer


class TreeShapInterventionalExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="TreeSHAPinterventional",
            type=["BlackBox", "WhiteBox"],
            categories=["Classification", "Regression"],
            explanations="both",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[DataTypeModelExplainer(DataType.TABULAR, TreeShap)],
        )

    def build(self, model: Model, data: ModelData):
        if not self.meta_data:
            raise Errors.METADATA_NOT_INSTANCE_OF_MODEL_METADATA

        self.build_result = TreeShap(
            model.handler, feature_names=self.meta_data.feature_names
        )

    def get_shap_values(self, x_test):
        self.build_result.fit(x_test)
        shap = self.build_result.explain(x_test, check_additivity=False)
        return np.array(shap.shap_values)
