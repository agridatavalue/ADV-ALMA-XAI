import numpy as np

from .model_metadata import ModelMetaData
from .explainers.response_data import FeatureImportance, FeatureDescription
from .explainers.response_data import PartialDependence, ExplainerResponseData
from .explainers.response_data import ConfusionMatrix, IndividualConditionalExpectations
from .explainers.response_data import ModelPerformance, ModelPerformanceMetrics, Heatmap


class ExplainerGuide:
    _meta_data: ModelMetaData

    def __init__(self, meta_data: ModelMetaData):
        self._meta_data = meta_data

    def get_explainers(self) -> list[ExplainerResponseData]:
        list_to_return:list[ExplainerResponseData] = []
        if self._meta_data.is_image:
            list_to_return.append(Heatmap())
            if self._meta_data.feature_descriptions:
                list_to_return.append(FeatureDescription())

        if self._meta_data.is_tabular:
            if self._meta_data.is_classification or self._meta_data.is_regression:
                list_to_return += [
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
                    IndividualConditionalExpectations(),
                ]
            if self._meta_data.is_classification:
                list_to_return += [ConfusionMatrix()]

        return list_to_return
