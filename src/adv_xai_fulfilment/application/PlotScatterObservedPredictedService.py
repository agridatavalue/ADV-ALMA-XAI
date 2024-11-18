import os
import numpy as np

from ..domain.model.Model import Model
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
    ) -> dict:
        model: Model = self.model_loader_service.load_from(explainer_identifier.model)

        data = self.data_loader_service.load_data(
            folder_path=explainer_identifier.data,
            bucket_name=os.getenv("DATA_FOLDER_PATH"),
        )

        X_test = np.array(data.get("x"))
        y_test = np.array(data.get("y"))

        return {"y_observed": y_test, "y_predicted": model.handler.predict(X_test)}
