from abc import ABC, abstractmethod

from ...domain.model.model import Model
from ...domain.model.data_type import DataType
from ...domain.model.model_data import ModelData
from ...domain.model.model_metadata import ModelMetaData
from ...domain.model.explainer_identifier import ExplainerIdentifier


class AbstractGeneratorService(ABC):
    @abstractmethod
    def generate(
        self,
        *,
        request: ExplainerIdentifier,
        meta_data: ModelMetaData,
        selected_model: Model,
        data: ModelData,
    ) -> list[any]: ...

    @staticmethod
    @abstractmethod
    def handled_type() -> DataType: ...
