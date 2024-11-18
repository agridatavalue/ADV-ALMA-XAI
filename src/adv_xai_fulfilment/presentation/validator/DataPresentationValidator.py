from .AbstractValidator import AbstractValidator


class DataPresentationValidator(AbstractValidator):
    def validate_and_sanitize_feature_description(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        return request

    def validate_and_sanitize_feature_importance(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_folder_data(request.get("data"))
        return request

    def validate_and_sanitize_model_performance(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_folder_data(request.get("data"))
        self._validate_metadata(request.get("meta_data"))
        return request

    def validate_and_sanitize_model_performance_metric(
        self, request: dict = {}
    ) -> dict:
        self._validate_model(request.get("model"))
        self._validate_metadata(request.get("meta_data"))
        return request

    def validate_and_sanitize_scatter(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_folder_data(request.get("data"))
        return request
