from ..domain.model.model_data import ModelData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..domain.model.explainers.response_data import DataFeaturesAndAverageScore

class DataFeaturesAverageScoreService:
    _data_loader_service: DataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()

    def get_data(self, expl_id:ExplainerIdentifier) -> DataFeaturesAndAverageScore:
        data: ModelData = self._data_loader_service.load_data(expl_id)

        to_ret = DataFeaturesAndAverageScore()
        for f, v in data.x.mean().to_dict().items():
            to_ret.add_feature(name=f, score=v)
        return to_ret