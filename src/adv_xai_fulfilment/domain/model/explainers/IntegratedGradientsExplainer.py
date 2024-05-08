from alibi.explainers import IntegratedGradients

from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class IntegratedGradientsExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="IntegratedGradients",
            type=["BlackBox"],
            category=["Classification"],
            explanations="local",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TEXT, IntegratedGradients),
                DataTypeModelExplainer(DataTypeModel.IMAGE, IntegratedGradients),
                DataTypeModelExplainer(DataTypeModel.TABULAR, IntegratedGradients),
            ],
        )
