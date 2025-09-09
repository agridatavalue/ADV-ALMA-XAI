import numpy as np

from logger import get_logger
from ..domain.model.model import Model
from ..domain.model.model_data import ModelData
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainers.response_data import LiftCurve
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.data_loader_service import DataLoaderService
from ..infrastructure.service.model_loader_service import ModelLoaderService
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService

logger = get_logger()

class LiftCurveService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, expl_id: ExplainerIdentifier) -> LiftCurve:
        data: ModelData = self._data_loader_service.load_data(expl_id)

        model_metadata: ModelMetaData = (
            self._metadata_loader_service.load_model_metadata(expl_id)
        )
        if not expl_id.prediction_target:
            logger.debug(
                f"empty prediction target, setting default as {model_metadata.first_target_name}"
            )
            expl_id.prediction_target = model_metadata.first_target_name
        
        selected_model: Model = self._model_loader_service.load_from(
            expl_id, meta_data=model_metadata
        )

        y_pred_prob = selected_model.handler.predict_proba(data.x)
        if y_pred_prob.ndim == 2:
            y_pred_prob = y_pred_prob[:, 1]

        sorted_indices = np.argsort(y_pred_prob)[::-1]
        sorted_y_test = np.array(data.y)[sorted_indices]

        cumulative_positives_model = np.cumsum(sorted_y_test)

        y_values = np.array(data.y).flatten()  # Ensure y is 1D
        total_positives = np.sum(y_values)
        cumulative_positives_random = np.arange(1, len(y_values) + 1) * (total_positives / len(y_values))

        return (
            LiftCurve()
            .set_lift_curve_data(np.arange(1, len(data.y) + 1))
            .set_cumulative_positives_model(cumulative_positives_model)
            .set_cumulative_positives_random(cumulative_positives_random)
        )