from .ModelMetaData import ModelMetaData

from .explainers.responseData.ExplainerResponseData import ExplainerResponseData

from .explainers.responseData.ModelPerformance import ModelPerformance
from .explainers.responseData.PartialDependence import PartialDependence
from .explainers.responseData.FeatureImportance import FeatureImportance
from .explainers.responseData.FeatureDescription import FeatureDescription
from .explainers.responseData.ModelPerformanceMetrics import ModelPerformanceMetrics


class ExplainerGuide:
    _meta_data: ModelMetaData

    def __init__(self, meta_data: ModelMetaData):
        self._meta_data = meta_data

    def get_explainers(self) -> list[ExplainerResponseData]:
        if self._meta_data.is_image:
            return [FeatureImportance, FeatureDescription]

        if self._meta_data.is_tabular:
            if self._meta_data.is_classification or self._meta_data.is_regression:
                return [
                    ModelPerformance,
                    PartialDependence,
                    FeatureImportance,
                    FeatureDescription,
                    ModelPerformanceMetrics,
                ]

        return []
