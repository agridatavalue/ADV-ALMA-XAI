import os
import logging
from dotenv import load_dotenv

from ..domain.model.Model import Model
from ..domain.model.explainers import all as all_class_explainers
from ..domain.model.explainers.Explainer import Explainer
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService

load_dotenv()


class ExplainerGeneratorService:
    _dataLoaderService: DataLoaderService
    _modelLoaderService: ModelLoaderService

    def __init__(self):
        self._dataLoaderService = DataLoaderService()
        self._modelLoaderService = ModelLoaderService()

    def generate_explainer(
        self,
        pilot: str,
        model_filename: str,
        metadata_filename: str,
        data_filename: str = None,
    ) -> list[Explainer]:
        assert isinstance(pilot, str)
        assert isinstance(model_filename, str)
        assert isinstance(metadata_filename, str)

        logging.info("downloading model and metadata")
        selected_model: Model = self._modelLoaderService.load_from(
            os.path.join(os.getenv("MODEL_FOLDER_PATH"), model_filename)
        )

        meta_data: dict = self._dataLoaderService.load_meta_data(
            os.path.join(os.getenv("MODEL_FOLDER_PATH"), metadata_filename)
        )

        data = self._dataLoaderService.load_data(
            os.path.join(os.getenv("DATA_FOLDER_PATH"), data_filename)
        )

        logging.info("selecting the matching Explainers")
        all_explainers_available: list[Explainer] = [c() for c in all_class_explainers]
        possible_explainers: list[Explainer] = [
            expl.set_meta_data(meta_data)
            for expl in all_explainers_available
            if expl.can_match_with(selected_model, meta_data)
        ]

        logging.info("creating the Explainer builds")
        for explainer in possible_explainers:
            explainer.build(model=selected_model, data=data)
            self._modelLoaderService.upload_to(
                os.path.join(os.getenv("EXPLAINER_FOLDER_PATH"), pilot),
                explainer,
            )

        return possible_explainers
