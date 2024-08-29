from ..application.PlotScatterObservedPredictedService import (
    PlotScatterObservedPredictedService,
)
from ..application.FeatureImportanceService import FeatureImportanceService


class DataPresentations:
    fi_service: FeatureImportanceService
    ps_service: PlotScatterObservedPredictedService

    def __init__(self):
        self.ps_service = PlotScatterObservedPredictedService()
        self.fi_service = FeatureImportanceService()

    def genarate_feature_importance(self, model_file_name: str) -> dict:
        assert isinstance(model_file_name, str)
        return self.fi_service.genarate_data_for_pilot(model_file_name)

    def genarate_performance_scatter_plot(self, model_file_name: str) -> dict:
        assert isinstance(model_file_name, str)
        return self.ps_service.genarate_data_for_pilot(model_file_name)
