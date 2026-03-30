from urllib.parse import urljoin

from logger import get_logger
from ..model.model_data import ModelData
from ...infrastructure.helper import Helper
from ..model.explainers.response_data import Heatmap
from ..model.explainer_identifier import ExplainerIdentifier
from ...infrastructure.repository import HeatmapImageGeneratorRepository
from ...infrastructure.service.data_loader_service import DataLoaderService
from ...infrastructure.service.explainer_repository_service import (
    ExplainerRepositoryService,
)

logger = get_logger()

class HeatmapComponentService:
    _data_loader_service: DataLoaderService
    _explainer_repository_service: ExplainerRepositoryService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._explainer_repository_service = ExplainerRepositoryService()
        self._heatmap_generator_repository = HeatmapImageGeneratorRepository()

    def generate_data(self, expl_id: ExplainerIdentifier) -> Heatmap:
        images: list[ModelData] = self._data_loader_service.load_images(expl_id)
        logger.debug(f"Loaded {len(images)} images")

        response = Heatmap()
        for current_img in images:
            logger.debug(f"Processing image {current_img.image_path}")
            heatmap_locale_filepath: str = self._heatmap_generator_repository.generate(
                current_img.image_path, expl_id.get_model_locale_filepath()
            )
            
            heatmap_filepath: str = self._explainer_repository_service.upload_file(
                expl_id, heatmap_locale_filepath
            )
            
            response.add(urljoin(Helper.get_folder_for_bucket_data(), heatmap_filepath))

        logger.debug(f"Generated {len(response.heatmaps)} heatmaps")
        return response
