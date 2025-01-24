from explainerdashboard import RegressionExplainer as DashRegressionExplainer


from ..DataType import DataType
from .Explainer import Explainer
from .DataTypeModelExplainer import DataTypeModelExplainer
from src.adv_xai_fulfilment.infrastructure.Constants import Errors


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

    def build(self, model, data: dict):
        assert isinstance(data, dict), Errors.DATA_NOT_DICT
        self.build_result = DashRegressionExplainer(model, data.get("x"), data.get("y"))
