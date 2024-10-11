import os
import numpy as np

from ..domain.model.Model import Model
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService


class PlotScatterObservedPredictedService:
    data_loader_service: DataLoaderService
    model_loader_service: ModelLoaderService

    def __init__(self):
        self.data_loader_service = DataLoaderService()
        self.model_loader_service = ModelLoaderService()

    def genarate_data_for_pilot(self, model_file_name: str) -> dict:
        model: Model = self.model_loader_service.load_from(model_file_name)

        data = self.data_loader_service.load_data(
            folder_path="crop", bucket_name=os.getenv("DATA_FOLDER_PATH")
        )

        X_test = np.array(data.get("x"))
        y_test = np.array(data.get("y"))

        return {"y_observed": y_test, "y_predicted": model.handler.predict(X_test)}
