from .abstract_validator import AbstractValidator


class DataPresentationValidator(AbstractValidator):
    def validate_and_sanitize_get_image(self, request: dict = {}) -> dict:
        assert isinstance(request.get("filename"), str), "filename must be provided"
        self._validate_pilot(request.get("pilot"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_heatmap(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_pilot(request.get("pilot"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_feature_description(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_feature_importance(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_pilot(request.get("pilot"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_model_performance(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_model_performance_metrics(
        self, request: dict = {}
    ) -> dict:
        self._validate_model(request.get("model"))
        self._validate_pilot(request.get("pilot"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_scatter(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_data_source_types(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_partial_dependence(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_pilot(request.get("pilot"))
        self._validate_prediction_target_str(request.get("prediction_target"))
        assert isinstance(request.get("feature"), str), "feature must be a string"
        return self._merge_with_default_values(request)

    def validate_and_sanitize_confusion_matrix(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_pilot(request.get("pilot"))
        return self._merge_with_default_values(request)
