import numpy as np

from ..domain.model.model_data import ModelData
from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import DataDistribution


class DataDistrubutionService(AbstractModelService):
    def get_data(self, expl_id: ExplainerIdentifier, bin_size: int) -> DataDistribution:
        context = self.get_context(expl_id)
        
        context.model_data.y_predict = context.model.handler.predict(context.model_data.x_train)

        if context.model_metadata.is_regression:
            return self._get_regression_data(context.model_data, bin_size)
        elif context.model_metadata.is_classification:
            return self._get_classification_data(context.model_data, bin_size)

        raise Exception('Cannot determine the type of the model')
    
    def _get_classification_data(self, data: ModelData, bin_size: int) -> DataDistribution:
        class_counts = data.y.value_counts().sort_index()
        return DataDistribution().set_bin_edges(class_counts.index.tolist()).set_counts(class_counts.values.tolist())
    
    def _get_regression_data(self, data: ModelData, bin_size: int) -> DataDistribution:
        counts, bin_edges = np.histogram(data.y_predict, bins=bin_size, density=True)
    
        return DataDistribution().set_bin_edges(bin_edges.tolist()).set_counts(counts.tolist())
    
    