import os
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

    def __init__(self) -> None:
        self._dataLoaderService = DataLoaderService()
        self._modelLoaderService = ModelLoaderService()

    def generate_explainer(
        self,
        pilot: str,
        data_filename: str,
        model_filename: str,
        metadata_filename: str,
    ) -> list[Explainer]:
        # load data from server
        selected_model: Model = self._modelLoaderService.loadFrom(
            os.path.join(os.getenv("MODEL_FOLDER_PATH"), model_filename)
        )

        meta_data = self._dataLoaderService.loadMetaData(
            os.path.join(os.getenv("MODEL_FOLDER_PATH"), metadata_filename)
        )

        all_explainers_available: list[Explainer] = [c() for c in all_class_explainers]

        # select the matching Explainers
        possible_explainers: list[Explainer] = [
            expl
            for expl in all_explainers_available
            if expl.canMatchWith(selected_model, meta_data)
        ]

        # create the explainers
        for explainer in possible_explainers:
            explainer.build_and_save_on_persistence(
                os.path.join(os.getenv("EXPLAINER_FOLDER_PATH"), pilot)
            )

        return explainer


"""
data = self._dataLoaderService.loadData(data)
metaData = self._dataLoaderService.loadMetaData(metadata)
"""
