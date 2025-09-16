import pickle
from abc import ABC
from typing import Optional

from ..model import Model
from ..model_data import ModelData
from ..model_metadata import ModelMetaData
from ..model_category import ModelCategory
from ....infrastructure.constants import Errors
from .datatype_model_explainer import DataTypeModelExplainer


class Explainer(ABC):
    name: str
    type: list[str]
    category: list[ModelCategory]
    explanations: str
    is_distributed: bool
    train_set_required: bool
    has_categorical_features: bool
    data_type_explainers: list[DataTypeModelExplainer]

    meta_data: Optional[ModelMetaData]
    build_result: Optional[object]
    

    def __init__(
        self,
        name: str,
        type: list[str],
        categories: list[str],
        explanations: str,
        is_distributed: bool,
        train_set_required: bool,
        has_categorical_features: bool,
        data_type_explainers: list[DataTypeModelExplainer],
    ):
        super().__init__()
        self.name = name
        self.type = type
        self.explanations = explanations
        self.is_distributed = is_distributed
        self.train_set_required = train_set_required
        self.data_type_explainers = data_type_explainers
        self.has_categorical_features = has_categorical_features
        self.categories = [
            ModelCategory.from_string(category) for category in categories
        ]

        self.meta_data = None
        self.build_result = None

    @property
    def file_name(self) -> str:
        return f"{self.name}.pkl"

    def load(self, path: str):
        if not (path or "").endswith(".pkl"):
            raise ValueError(Errors.PATH_NOT_PICKLE)
        
        with open(path, "rb") as file:
            self.build_result = pickle.load(file)

    def can_match_with(self, model: Model, meta_data: ModelMetaData) -> bool:
        if not isinstance(meta_data, ModelMetaData):
            return False

        return (
            meta_data.model_type in self.type
            and meta_data.model_category in self.categories
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

    def build(self, model, data: ModelData):
        raise NotImplementedError("Not implemented yet.")

    def train_with_partner_data(self, partner_data: dict) -> bool:
        return False

    def ask_to_llm(self, request: str) -> str:
        return ""

    def __repr__(self) -> str:
        return f'<Explainer name="{self.name}">'
