import logging

from ...domain.model.model import Model
from ...domain.model.data_type import DataType
from ...domain.model.model_data import ModelData
from ...domain.model.model_metadata import ModelMetaData
from .abstract_generator_service import AbstractGeneratorService
from ...domain.model.explainer_identifier import ExplainerIdentifier
from ...domain.service.heatmap_component_service import HeatmapComponentService


class ImageGeneratorService(AbstractGeneratorService):
    _heatmap_component_service = HeatmapComponentService

    def __init__(self):
        super().__init__()
        self._heatmap_component_service = HeatmapComponentService()

    def handled_type() -> DataType:
        return DataType.IMAGE

    def generate(
        self,
        *,
        request: ExplainerIdentifier,
        meta_data: ModelMetaData,
        selected_model: Model,
        data: ModelData,
    ) -> list[any]:
        logging.debug(f"generating image explainers for {str(request)}")
        return [self._heatmap_component_service.generate_data(request)]
