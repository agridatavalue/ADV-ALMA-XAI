import os
from dotenv import load_dotenv

from src.adv_xai_fulfilment.domain.model.Model import Model
from src.adv_xai_fulfilment.domain.model.Explainer import Explainer
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)
from src.adv_xai_fulfilment.infrastructure.service.ModelLoaderService import (
    ModelLoaderService,
)

load_dotenv()


class TrainerService:
    _dataLoaderService: DataLoaderService
    _modelLoaderService: ModelLoaderService

    def __init__(self) -> None:
        self._dataLoaderService = DataLoaderService()
        self._modelLoaderService = ModelLoaderService()

    def train(
        self, modelName: str, pilot: str, data: str, metadata: str
    ) -> list[Explainer]:
        # load data from server
        selected_model: Model = self._dataLoaderService.loadModelFrom(modelName)

        # load models
        all_models: list[Model] = self._modelLoaderService.loadFrom(
            os.get("MODELS_FILE_PATH")
        )

        # select the matching models
        possible_explainers: list[Explainer] = [
            Explainer(model)
            for model in all_models
            if selected_model.canMatchWith(model)
        ]

        # create the explainers
        for explainer in possible_explainers:
            explainer.build_and_save_on_persistence()

        return explainer


"""
data = self._dataLoaderService.loadData(data)
metaData = self._dataLoaderService.loadMetaData(metadata)
"""
