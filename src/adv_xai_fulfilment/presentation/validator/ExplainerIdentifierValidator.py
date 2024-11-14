from .AbstractValidator import AbstractValidator


class ExplainerIdentifierValidator(AbstractValidator):
    def validate_questions_(self, request: dict = {}) -> bool:
        self._validate_model(request.get("model"))
        self._validate_prediction_target(request.get("prediction_target"))
        return True

    def validate_feedback_(self, request: dict = {}) -> bool:
        self._validate_model(request.get("model"))
        self._validate_prediction_target(request.get("prediction_target"))

        assert request.get("responses", []), "Responses must be a list of dictionaries"
        assert all(
            isinstance(response, dict) for response in request.get("responses")
        ), "Response must be a dictionary"
        return True
