from .abstract_validator import AbstractValidator

class KpiDataValidator(AbstractValidator):
    def validate_and_sanitize_model_feedback(self, request: dict = {}) -> dict:
        self._validate_model(request.get("model", ""))
        return request