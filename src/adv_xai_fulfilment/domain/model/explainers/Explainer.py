import pickle
from abc import ABC

from ..Model import Model
from ..ModelMetaData import ModelMetaData
from ....infrastructure.Constants import Errors
from .DataTypeModelExplainer import DataTypeModelExplainer


class Explainer(ABC):
    name: str
    type: list[str]
    category: list[str]
    explanations: str
    is_distributed: bool
    train_set_required: bool
    has_categorical_features: bool
    data_type_explainers: list[DataTypeModelExplainer]

    meta_data: ModelMetaData
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
        super().__init__()
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

    @property
    def file_name(self) -> str:
        return f"{self.name}.pkl"

    def load(self, path: str):
        assert (path or "").endswith(".pkl"), Errors.PATH_NOT_PICKLE
        with open(path, "rb") as file:
            self.build_result = pickle.load(file)

    def can_match_with(self, model: Model, meta_data: ModelMetaData) -> bool:
        if not isinstance(meta_data, ModelMetaData):
            return False

        return (
            meta_data.model_type in self.type
            and meta_data.model_category in self.category
            and (
                meta_data.data_type
                in [dt.data_type for dt in self.data_type_explainers]
            )
        )

    def set_meta_data(self, meta_data: ModelMetaData):
        assert isinstance(
            meta_data, ModelMetaData
        ), "meta_data must be a ModelMetaData instance."
        self.meta_data = meta_data
        return self

    def build(self, model, data: dict):
        raise NotImplementedError("Not implemented yet.")

    def train_with_pilot_data(self, pilot_data: dict) -> bool:
        return False

    def ask_to_llm(self, request: str) -> str:
        return ""

    def __repr__(self) -> str:
        return f'<Explainer name="{self.name}">'
