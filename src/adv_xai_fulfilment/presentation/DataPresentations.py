import numpy as np
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

    def genarate_feature_description(self, meta_data_filename: str) -> dict:
        assert isinstance(meta_data_filename, str)
        return self.fi_service.genarate_feature_description(meta_data_filename)

    def genarate_feature_importance(
        self, model_file_name: str, meta_data_filename: str
    ) -> dict:
        assert isinstance(model_file_name, str)
        data: np.array = self.fi_service.genarate_data(
            model_file_name, meta_data_filename
        )
        return {"data": data.tolist()}

    def genarate_performance_scatter_plot(self, model_file_name: str) -> dict:
        assert isinstance(model_file_name, str)
        return self.ps_service.genarate_data_for_pilot(model_file_name)
