import logging
from ..model.model_data import ModelData
from ..model.explainers.response_data import Heatmap
from ..model.explainer_identifier import ExplainerIdentifier
from ...infrastructure.service.DataLoaderService import DataLoaderService
from ...infrastructure.repository import HeatmapImageGeneratorRepository


class HeatmapComponentService:
    _data_loader_service: DataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._heatmap_generator_repository = HeatmapImageGeneratorRepository()

    def generate_data(self, expl_id: ExplainerIdentifier) -> Heatmap:
        images: list[ModelData] = self._data_loader_service.load_images(expl_id)
        logging.debug(f"Loaded {len(images)} images")

        response = Heatmap()
        for current_img in images:
            logging.debug(f"Processing image {current_img.image_path}")
            heatmap_filepath: str = self._heatmap_generator_repository.generate(
                current_img.image_path, expl_id.get_model_locale_filepath()
            )
            response.add(heatmap_filepath)

        logging.debug(f"Generated {len(response.heatmaps)} heatmaps")
        return response
