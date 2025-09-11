from ..domain.model.model_data import ModelData
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.data_loader_service import DataLoaderService
from ..domain.model.explainers.response_data import DataFeaturesAndAverageScore
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService

class DataFeaturesAverageScoreService:
    _data_loader_service: DataLoaderService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, expl_id:ExplainerIdentifier) -> DataFeaturesAndAverageScore:
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=expl_id
        )
        
        data: ModelData = self._data_loader_service.load_data(expl_id)
        data.calculate_x_and_y_predict_and_x_and_y_train(meta_data.feature_names, meta_data.target_names[0])

        to_ret = DataFeaturesAndAverageScore()
        for f, v in data.x.mean().to_dict().items():
            to_ret.add_feature(name=f, score=v)
        return to_ret