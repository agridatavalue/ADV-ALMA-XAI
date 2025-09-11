import numpy as np

from ..domain.model.model import Model
from ..domain.model.model_data import ModelData
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.data_loader_service import DataLoaderService
from ..infrastructure.service.model_loader_service import ModelLoaderService
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService


class PlotScatterObservedPredictedService:
    data_loader_service: DataLoaderService
    model_loader_service: ModelLoaderService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self.data_loader_service = DataLoaderService()
        self.model_loader_service = ModelLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def genarate_data_for_partner(
        self, explainer_identifier: ExplainerIdentifier
    ) -> dict["y_observed" : np.ndarray, "y_predicted" : np.ndarray]:
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=explainer_identifier
        )
        
        model: Model = self.model_loader_service.load_from(explainer_identifier)

        data: ModelData = self.data_loader_service.load_data(explainer_identifier)
        data.calculate_x_and_y_predict_and_x_and_y_train(meta_data.feature_names, meta_data.target_names[0])
        
        X_test = np.array(data.x_predict)
        y_test = np.array(data.y_predict)

        return {"y_observed": y_test, "y_predicted": model.handler.predict(X_test)}
