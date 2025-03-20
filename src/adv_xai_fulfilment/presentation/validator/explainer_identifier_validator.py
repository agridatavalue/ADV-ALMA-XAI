from .abstract_validator import AbstractValidator


class ExplainerIdentifierValidator(AbstractValidator):
    def validate_and_sanitize_questions_(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        self._validate_prediction_target_str(request.get("prediction_target"))
        return self._merge_with_default_values(request)

    def validate_and_sanitize_feedback_(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        self._validate_prediction_target_str(request.get("prediction_target"))

        assert request.get("responses", []), "Responses must be a list of dictionaries"
        assert all(
            isinstance(response, dict) for response in request.get("responses")
        ), "Response must be a dictionary"
        return self._merge_with_default_values(request)

    def validate_and_sanitize_partner_feedback(self, request:dict = {}) -> dict:
        self._validate_model(request.get("model"))
        self._validate_partner(request.get("partner"))
        return self._merge_with_default_values(request)
