from explainerdashboard import RegressionExplainer as DashRegressionExplainer


from ..data_type import DataType
from .explainer import Explainer
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer


class RegressionExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="RegressionExplainer",
            type=["BlackBox"],
            categories=["Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=False,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, DashRegressionExplainer)
            ],
        )

    def build(self, model, data: ModelData):
        self.build_result = DashRegressionExplainer(model, data.x, data.y)
