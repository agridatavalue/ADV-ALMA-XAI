import numpy as np

from ..domain.model.model_data import ModelData
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import DataDistribution
from ..infrastructure.service.data_loader_service import DataLoaderService
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService

class DataDistrubutionService:
    _data_loader_service: DataLoaderService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()

    def get_data(self, expl_id: ExplainerIdentifier, bin_size: int) -> DataDistribution:
        data: ModelData = self._data_loader_service.load_data(expl_id)
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=expl_id
        )

        if meta_data.is_regression:
            return self._get_regression_data(data, bin_size)
        elif meta_data.is_classification:
            return self._get_classification_data(data, bin_size)

        raise Exception('Cannot determine the type of the model')
    
    def _get_classification_data(self, data: ModelData, bin_size:int) -> DataDistribution:
        class_counts = data.y.value_counts().sort_index()
        return DataDistribution().set_bin_edges(class_counts.index.tolist()).set_counts(class_counts.values.tolist())
    
    def _get_regression_data(self, data: ModelData, bin_size:int) -> DataDistribution:
        counts, bin_edges = np.histogram(data.y, bins=bin_size, density=True)
    
        return DataDistribution().set_bin_edges(bin_edges.tolist()).set_counts(counts.tolist())
    
    