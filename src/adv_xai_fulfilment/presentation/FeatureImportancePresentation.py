from ..application.FeatureImportanceService import FeatureImportanceService


class FeatureImportancePresentation:
    fi_service: FeatureImportanceService

    def __init__(self):
        self.fi_service = FeatureImportanceService()

    def genarate_data_for_pilot(self, model_file_name: str) -> dict:
        assert isinstance(model_file_name, str)

        return self.fi_service.genarate_data_for_pilot(model_file_name)
