import os
import logging
import pandas as pd
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

        logging.info("downloading model")
        selected_model: Model = self._modelLoaderService.load_from(model_filename)
        logging.info("downloading meta data")
        meta_data: dict = self._dataLoaderService.load_meta_data(metadata_filename)
        logging.info("downloading data if present")
        data: dict[str, pd.DataFrame] = self._dataLoaderService.load_data(data_filename)

        logging.debug("creating the matching Explainers")
        all_explainers_available: list[Explainer] = [c() for c in all_class_explainers]
        logging.info("selecting the matching Explainers")
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
