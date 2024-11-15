from .AbstractValidator import AbstractValidator


class DataPresentationValidator(AbstractValidator):
    def validate_feature_description(self, request: dict = {}) -> bool:
        self._validate_model(request.get("model"))
        return True

    def validate_feature_importance(self, request: dict = {}) -> bool:
        self._validate_model(request.get("model"))
        self._validate_prediction_target(request.get("prediction_target"))
        return True
