import os
import logging
import pandas as pd
from dotenv import load_dotenv

from ..domain.model.Model import Model
from ..infrastructure.Constants import Errors
from ..domain.model.explainers.Explainer import Explainer
from ..domain.model.ExplainerMetaData import ExplainerMetaData
from ..domain.service.ExplainerRetriever import ExplainerRetriever
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..domain.service.ModelPerformanceMetricServiceComponent import (
    ModelPerformanceMetricServiceComponent,
)

load_dotenv()


class ExplainerGeneratorService:
    _dataLoaderService: DataLoaderService
    _modelLoaderService: ModelLoaderService
    _explainer_retriever: ExplainerRetriever

    _mpm_service: ModelPerformanceMetricServiceComponent

    def __init__(self):
        self._dataLoaderService = DataLoaderService()
        self._modelLoaderService = ModelLoaderService()
        self._explainer_retriever = ExplainerRetriever()
        self._mpm_service = ModelPerformanceMetricServiceComponent()

    def generate_explainer(
        self,
        pilot: str,
        model_filename: str,
        metadata_filename: str,
        data_folder: str = None,
    ) -> list[Explainer]:
        assert isinstance(pilot, str), Errors.PILOT_NOT_STRING
        assert isinstance(model_filename, str), Errors.PILOT_NOT_STRING
        assert isinstance(metadata_filename, str), Errors.METADATA_FILENAME_NOT_STRING

        logging.debug("downloading model")
        selected_model: Model = self._modelLoaderService.load_from(model_filename)
        logging.debug("downloading meta data")
        meta_data: dict = self._dataLoaderService.load_meta_data(metadata_filename)
        logging.debug("downloading data if present")
        data: dict[str, pd.DataFrame] = self._dataLoaderService.load_data(
            file_path=data_folder, bucket_name=os.getenv("DATA_FOLDER_PATH")
        )

        logging.debug("selecting the matching Explainers")
        possible_explainers: list[Explainer] = self._explainer_retriever.get_by_data(
            selected_model, meta_data
        )
        logging.info(
            f"found {len(possible_explainers)} explainers: {possible_explainers}"
        )

        created_explainers: list[Explainer] = []
        for explainer in possible_explainers:
            logging.debug(f"creating the explainer {explainer.name} builds")
            try:
                explainer.build(model=selected_model, data=data)
                self._modelLoaderService.upload_to(
                    model_path=os.getenv("EXPLAINER_FOLDER_PATH"),
                    pilot=pilot,
                    explainer=explainer,
                )
                created_explainers.append(explainer)
            except Exception as e:
                logging.error(
                    f"error building the explainer {explainer.name}: {str(e)}"
                )

        expl_metadata = ExplainerMetaData(
            possible_explainers=created_explainers,
            metrics=self._mpm_service.get_metrics(model=selected_model, data=data),
        )
        logging.debug("uploading the explainer metadata")
        if expl_metadata.data_are_ok:
            self._dataLoaderService.upload(explainer_data=expl_metadata, pilot=pilot)

        return created_explainers

    def ask_to_explainer(self, pilot: str, request: str, explainer_name: str):
        assert isinstance(pilot, str), Errors.PILOT_NOT_STRING
        assert isinstance(request, str), Errors.REQUEST_NOT_STRING
        assert isinstance(explainer_name, str), Errors.EXPLAINER_NAME_NOT_STRING

        explainer: Explainer = self._explainer_retriever.get_by_name(explainer_name)
        pilot_data = self._modelLoaderService.download_for(pilot=pilot)
        explainer.train_with_pilot_data(pilot_data)
        return explainer.ask_to_llm(request)
