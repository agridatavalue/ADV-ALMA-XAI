from ..application.PlotScatterObservedPredictedService import (
    PlotScatterObservedPredictedService,
)


class PlotScatterObservedPredictedPresentation:
    ps_service: PlotScatterObservedPredictedService

    def __init__(self):
        self.ps_service = PlotScatterObservedPredictedService()

    def genarate_data_for_pilot(self, model_file_name: str) -> dict:
        assert isinstance(model_file_name, str)

        return self.ps_service.genarate_data_for_pilot(model_file_name)
