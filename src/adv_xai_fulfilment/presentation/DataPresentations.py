import pandas as pd

from ..infrastructure.Constants import Errors
from ..application.PlotScatterObservedPredictedService import (
    PlotScatterObservedPredictedService,
)
from ..application.FeatureImportanceService import FeatureImportanceService
from ..application.ModelPerformanceMetricService import ModelPerformanceMetricService


class DataPresentations:
    feature_importance_service: FeatureImportanceService
    model_performance_service: ModelPerformanceMetricService
    plot_scatter_service: PlotScatterObservedPredictedService

    def __init__(self):
        self.plot_scatter_service = PlotScatterObservedPredictedService()
        self.model_performance_service = ModelPerformanceMetricService()
        self.feature_importance_service = FeatureImportanceService()

    def genarate_feature_description(self, meta_data_filename: str) -> dict:
        assert isinstance(meta_data_filename, str), Errors.METADATA_FILENAME_NOT_STRING
        return self.feature_importance_service.genarate_feature_description(
            meta_data_filename
        )

    def genarate_feature_importance(
        self, meta_data_filename: str, pilot: str
    ) -> pd.DataFrame:
        return self.feature_importance_service.get_data(meta_data_filename, pilot=pilot)

    def genarate_performance_scatter_plot(self, model_file_name: str) -> dict:
        assert isinstance(model_file_name, str), Errors.MODEL_FILENAME_NOT_STRING
        return self.plot_scatter_service.genarate_data_for_pilot(model_file_name)

    def get_model_performance_metric(self, model_filename: str) -> dict:
        assert isinstance(model_filename, str), Errors.MODEL_FILENAME_NOT_STRING
        return self.model_performance_service.get_metrics(model_filename=model_filename)

    def genarate_model_performance(self, model_file_name: str) -> dict:
        assert isinstance(model_file_name, str), Errors.MODEL_FILENAME_NOT_STRING
        return self.model_performance_service.get_data(model_filename=model_file_name)
