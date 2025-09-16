from logger import get_logger
from ...domain.model.data_type import DataType
from ...domain.model.model_context import ModelContext
from .abstract_generator_service import AbstractGeneratorService
from ...domain.service.heatmap_component_service import HeatmapComponentService

logger = get_logger()

class ImageGeneratorService(AbstractGeneratorService):
    _heatmap_component_service = HeatmapComponentService

    def __init__(self):
        super().__init__()
        self._heatmap_component_service = HeatmapComponentService()

    def handled_type() -> DataType:
        return DataType.IMAGE

    def generate(self, context: ModelContext) -> list:
        logger.debug(f"generating image explainers for {str(context.identifier)}")
        return [self._heatmap_component_service.generate_data(context.identifier)]
