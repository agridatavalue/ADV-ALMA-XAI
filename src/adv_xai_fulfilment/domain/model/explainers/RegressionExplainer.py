from explainerdashboard import RegressionExplainer

from .Explainer import Explainer
from .DataTypeModel import DataTypeModel
from .DataTypeModelExplainer import DataTypeModelExplainer


class RegressionExplainer(Explainer):

    def __init__(self):
        super().__init__(
            name="RegressionExplainer",
            type=["BlackBox"],
            category=["Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=False,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TABULAR, RegressionExplainer)
            ],
        )

    def build(self, model, data: dict):
        self.build_result = RegressionExplainer(model, data.get("x"), data.get("y"))
