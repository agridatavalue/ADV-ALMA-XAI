from alibi.explainers import TreeShap

from ..Model import Model
from ..DataType import DataType
from .Explainer import Explainer
from ....infrastructure.Constants import Errors
from .DataTypeModelExplainer import DataTypeModelExplainer


class TreeShapInterventionalExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="TreeSHAPinterventional",
            type=["WhiteBox"],
            categories=["Classification", "Regression"],
            explanations="both",
            is_distributed=False,
            train_set_required=None,
            has_categorical_features=True,
            data_type_explainers=[DataTypeModelExplainer(DataType.TABULAR, TreeShap)],
        )

    def build(self, model: Model, data: dict):
        if not self.meta_data:
            raise Errors.METADATA_NOT_INSTANCE_OF_MODEL_METADATA

        self.build_result = TreeShap(
            model.handler, feature_names=self.meta_data.feature_names
        )
