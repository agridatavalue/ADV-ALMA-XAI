import numpy as np

from ..domain.model.Model import Model
from ..domain.model.ModelData import ModelData
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService


class PlotScatterObservedPredictedService:
    data_loader_service: DataLoaderService
    model_loader_service: ModelLoaderService

    def __init__(self):
        self.data_loader_service = DataLoaderService()
        self.model_loader_service = ModelLoaderService()

    def genarate_data_for_pilot(
        self, explainer_identifier: ExplainerIdentifier
    ) -> dict["y_observed" : np.ndarray, "y_predicted" : np.ndarray]:
        model: Model = self.model_loader_service.load_from(explainer_identifier.model)

        data: ModelData = self.data_loader_service.load_data(explainer_identifier)

        X_test = np.array(data.x)
        y_test = np.array(data.y)

        return {"y_observed": y_test, "y_predicted": model.handler.predict(X_test)}
