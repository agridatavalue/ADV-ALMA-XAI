from shap import DeepExplainer, sample

from ..Model import Model
from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class DeepExplainerExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="DeepExplainer",
            type=["BlackBox"],
            category=["Classification", "Regression"],
            explanations="both",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, DeepExplainer),
                DataTypeModelExplainer(DataTypeModel.IMAGE, DeepExplainer),
            ],
        )

    def get_shap_values(self, model: Model, x_train, x_test):
        explainer = DeepExplainer(
            model.handler.predict,
            x_train,
        )
        return explainer.shap_values(x_test)
