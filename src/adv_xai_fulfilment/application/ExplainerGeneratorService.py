import os
import logging
import pandas as pd
from dotenv import load_dotenv

from ..domain.model.Model import Model
from ..domain.model.explainers.Explainer import Explainer
from ..domain.service.ExplainerRetriever import ExplainerRetriever
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService

load_dotenv()


class ExplainerGeneratorService:
    _dataLoaderService: DataLoaderService
    _modelLoaderService: ModelLoaderService
    _explainer_retriever: ExplainerRetriever

    def __init__(self):
        self._dataLoaderService = DataLoaderService()
        self._modelLoaderService = ModelLoaderService()
        self._explainer_retriever = ExplainerRetriever()

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

        logging.debug("downloading model")
        selected_model: Model = self._modelLoaderService.load_from(model_filename)
        logging.debug("downloading meta data")
        meta_data: dict = self._dataLoaderService.load_meta_data(metadata_filename)
        logging.debug("downloading data if present")
        data: dict[str, pd.DataFrame] = self._dataLoaderService.load_data(data_filename)

        logging.debug("selecting the matching Explainers")
        possible_explainers: list[Explainer] = self._explainer_retriever.get_by_data(
            selected_model, meta_data
        )
        logging.info(f"found {len(possible_explainers)} explainers")

        for explainer in possible_explainers:
            logging.debug(f"creating the explainer {explainer.name} builds")
            explainer.build(model=selected_model, data=data)
            self._modelLoaderService.upload_to(
                model_path=os.getenv("EXPLAINER_FOLDER_PATH"),
                pilot=pilot,
                explainer=explainer,
            )

        return possible_explainers

    def ask_to_explainer(self, pilot: str, request: str, explainer_name: str):
        assert isinstance(pilot, str)
        assert isinstance(request, str)
        assert isinstance(explainer_name, str)

        explainer: Explainer = self._explainer_retriever.get_by_name(explainer_name)
        pilot_data = self._modelLoaderService.download_for(pilot=pilot)
        explainer.train_with_pilot_data(pilot_data)
        return explainer.ask_to_llm(request)
