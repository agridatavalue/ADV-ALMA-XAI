from .AbstractValidator import AbstractValidator


class DataPresentationValidator(AbstractValidator):
    def validate_feature_description(self, request: dict = {}) -> bool:
        self._validate_model(request.get("model"))
        return True

    def validate_feature_importance(self, request: dict = {}) -> bool:
        self._validate_model(request.get("model"))
        self._validate_prediction_target_str(request.get("prediction_target"))
        return True

    def validate_and_sanitize_model_performance(self, data: dict = {}) -> dict:
        self._validate_model(data.get("model"))
        self._validate_folder_data(data.get("data"))
        self._validate_prediction_target_int(data.get("prediction_target", 0))

        return {
            **data,
            "prediction_target": int(data.get("prediction_target", 0)),
        }
