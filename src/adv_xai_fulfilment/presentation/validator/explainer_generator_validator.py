from .abstract_validator import AbstractValidator


class ExplainerGeneratorValidator(AbstractValidator):
    def validate_and_sanitize_build(self, data: dict) -> dict:
        self._validate_model(data.get("model"))
        self._validate_partner(data.get("partner"))
        self._validate_folder_data(data.get("data"))
        return data

    def validate_and_sanitize_ask(self, data: dict) -> dict:
        self._validate_partner(data.get("partner"))
        assert isinstance(data.get("request"), str), "Request must be a string"
        assert isinstance(data.get("explainer"), str), "Explainer must be a string"
        return data

    def validate_and_sanitize_get_data(self, data: dict) -> dict:
        self._validate_model(data.get("model"))
        self._validate_partner(data.get("partner"))
        return data
