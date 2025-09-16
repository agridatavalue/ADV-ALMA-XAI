from abc import ABC, abstractmethod

from ...domain.model.data_type import DataType
from ...domain.model.model_context import ModelContext


class AbstractGeneratorService(ABC):
    @abstractmethod
    def generate(self, context: ModelContext) -> list: ...

    @staticmethod
    @abstractmethod
    def handled_type() -> DataType: ...
