from .DataTypeModelExplainer import DataTypeModelExplainer


class Model:
    name: str
    type: list[str]
    category: list[str]
    explanations: str
    is_distributed: bool
    train_set_required: bool
    has_categorical_features: bool
    data_type_explainers: list[DataTypeModelExplainer]

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

    def canMatchWith(self, model) -> bool:
        return (
            self.type in model.type
            and self.category in model.category
            and self.data_type in model.datatype
        )

    def __repr__(self) -> str:
        return f'<Model name="{self.name}">'
