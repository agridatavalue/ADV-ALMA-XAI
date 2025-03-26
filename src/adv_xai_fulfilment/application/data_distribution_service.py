from ..domain.model.model_data import ModelData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import DataDistribution
from ..infrastructure.service.DataLoaderService import DataLoaderService

class DataDistrubutionService:
    _data_loader_service: DataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()

    def get_data(self, expl_id:ExplainerIdentifier) -> DataDistribution:
        data: ModelData = self._data_loader_service.load_data(expl_id)

        if expl_id.prediction_target not in data.x.columns:
            raise Exception('')

        data = df[target].dropna().tolist()  # Remove NaNs and convert to list
        return {"target_column": target, "data": data}