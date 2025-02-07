import numpy as np

from .model_metadata import ModelMetaData
from .explainers.responseData.model_performance import ModelPerformance
from .explainers.responseData.partial_dependence import PartialDependence
from .explainers.responseData.feature_importance import FeatureImportance
from .explainers.responseData.feature_description import FeatureDescription
from .explainers.responseData.explainer_response_data import ExplainerResponseData
from .explainers.responseData.model_performance_metrics import ModelPerformanceMetrics


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
                    ModelPerformance(),
                    PartialDependence(
                        feature_values=np.ndarray([], dtype=float),
                        pdp_values=np.ndarray([], dtype=float),
                        mean_effect=0.0,
                        std_effect=0.0,
                    ),
                    FeatureImportance(""),
                    FeatureDescription(),
                    ModelPerformanceMetrics(),
                ]

        return []
