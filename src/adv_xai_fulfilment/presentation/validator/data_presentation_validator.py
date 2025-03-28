from .abstract_validator import AbstractValidator


class DataPresentationValidator(AbstractValidator):
    def validate_and_sanitize_class_label_sizes(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)
    
    def validate_and_sanitize_targets(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)
    
    def validate_and_sanitize_data_distribution(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values({'bin_size': 30, **request})
    
    def validate_and_sanitize_data_features_and_average_score(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)
    
    def validate_and_sanitize_individual_conditional_expectations(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        self._validate_feature(request.get("feature"))
        return self._merge_with_default_values(request)
    
    def validate_and_sanitize_get_image(self, request: dict = {}) -> dict:
        assert isinstance(request.get("filename"), str), "filename must be provided"
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_heatmap(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_feature_description(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_feature_importance(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_model_performance(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_model_performance_metrics(
        self, request: dict = {}
    ) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_scatter(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_data_source_types(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_partial_dependence(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        self._validate_feature(request.get("feature"))
        self._validate_prediction_target_str(request.get("prediction_target"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_confusion_matrix(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)
