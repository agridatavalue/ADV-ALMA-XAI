from ..Model import Model
from .DataTypeModelExplainer import DataTypeModelExplainer


class Explainer:
    name: str
    type: list[str]
    category: list[str]
    explanations: str
    is_distributed: bool
    train_set_required: bool
    has_categorical_features: bool
    data_type_explainers: list[DataTypeModelExplainer]

    meta_data: dict
    build_result: any

    def __init__(
        self,
        name: str,
        type: list[str],
        category: list[str],
        explanations: str,
        is_distributed: bool,
        train_set_required: bool,
        has_categorical_features: bool,
        data_type_explainers: list[DataTypeModelExplainer],
    ):
        self.name = name
        self.type = type
        self.category = category
        self.explanations = explanations
        self.is_distributed = is_distributed
        self.train_set_required = train_set_required
        self.data_type_explainers = data_type_explainers
        self.has_categorical_features = has_categorical_features

        self.meta_data = None
        self.build_result = None

    def can_match_with(self, model: Model, meta_data: dict) -> bool:
        return (
            self.type in meta_data.get("modeltype")
            and self.category in meta_data.get("modelcategory")
            and meta_data.get("datatype")
            in [dt.data_type for dt in self.data_type_explainers]
        )

    def set_meta_data(self, meta_data: dict):
        self.meta_data = {
            **meta_data,
            "id": 1,  # TODO: Change for a unique id
            "name": self.name,
            "xplanationscope": "global",
            "xplainerparameters": "n/a",  # TODO: Change it
            "xplanationtype": "feature_importance",  # TODO: Change it
            "xplanationmetrics": "n/a",  # TODO: Change it
            "modelparameters": "n/a",  # TODO: Change it
            "modelspecifictype": "n/a",  # TODO: Change it
            "xaidependencies": ["numpy", "Scikit-learn", "alibi[ray]"],
        }
        return self

    def build(self, model, data: dict): ...

    def __repr__(self) -> str:
        return f'<Explainer name="{self.name}">'
