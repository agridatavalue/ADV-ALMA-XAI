import numpy as np

from .model_metadata import ModelMetaData
from .explainers.response_data import FeatureImportance, FeatureDescription
from .explainers.response_data import DataFeaturesAndAverageScore, LiftCurve
from .explainers.response_data import PartialDependence, ExplainerResponseData
from .explainers.response_data import DataSourceTypes, DataDistribution, Targets
from .explainers.response_data import AnomalyScore, FeatureImpact, AnomalyVsNormal
from .explainers.response_data import ConfusionMatrix, IndividualConditionalExpectations
from .explainers.response_data import ModelPerformance, ModelPerformanceMetrics, Heatmap


class ExplainerGuide:
    _meta_data: ModelMetaData

    def __init__(self, meta_data: ModelMetaData):
        self._meta_data = meta_data
        
    def get_model_category(self):
        return self._meta_data.model_category

    def get_explainers(self) -> list[ExplainerResponseData]:
        list_to_return:list[ExplainerResponseData] = []
        if self._meta_data.is_image:
            list_to_return.append(Heatmap())
            if self._meta_data.feature_descriptions:
                list_to_return.append(FeatureDescription())

        if self._meta_data.is_tabular:
            list_to_return += [DataSourceTypes()]
            if self._meta_data.is_classification or self._meta_data.is_regression:
                list_to_return += [
                    DataDistribution(),
                    PartialDependence(
                        feature_values=np.ndarray([], dtype=float),
                        pdp_values=np.ndarray([], dtype=float),
                        mean_effect=0.0,
                        std_effect=0.0,
                    ),
                    FeatureImportance(""),
                    ModelPerformanceMetrics(),
                    DataFeaturesAndAverageScore(),
                    IndividualConditionalExpectations(),
                    FeatureDescription(),
                ]
            if self._meta_data.is_classification:
                list_to_return += [ConfusionMatrix(), LiftCurve()]
            if self._meta_data.is_regression:
                list_to_return += [ModelPerformance(), Targets()]
                
            if self._meta_data.is_ts_anomaly_detection:
                if len(self._meta_data.target_names) > 0:
                    list_to_return += [
                        AnomalyScore(),
                        FeatureImpact(),
                        AnomalyVsNormal(),
                        ConfusionMatrix(),
                        FeatureImportance(''),
                        ModelPerformanceMetrics(),
                    ]

        return list_to_return

    def to_dict(self) -> dict:
        return {
            "endpoints": [
                {"url": r.corresponding_endpoint, "name": r.__class__.__name__}
                for r in self.get_explainers()
            ],
            "model_category": self.get_model_category()
        }