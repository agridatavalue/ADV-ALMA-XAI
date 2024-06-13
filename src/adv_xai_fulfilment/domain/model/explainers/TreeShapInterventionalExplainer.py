from alibi.explainers import TreeShap

from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class TreeShapInterventionalExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="TreeSHAPinterventional",
            type=["WhiteBox"],
            category=["Classification"],
            explanations="both",
            is_distributed=False,
            train_set_required=None,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, TreeShap)
            ],
        )
