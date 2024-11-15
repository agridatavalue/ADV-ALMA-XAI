from .AbstractValidator import AbstractValidator


class ExplainerGeneratorValidator(AbstractValidator):
    def validate_build(self, data: dict) -> bool:
        self._validate_model(data.get("model"))
        self._validate_pilot(data.get("pilot"))
        self._validate_metadata(data.get("metadata"))
        return True

    def validate_ask(self, data: dict) -> bool:
        self._validate_pilot(data.get("pilot"))
        assert isinstance(data.get("request"), str), "Request must be a string"
        assert isinstance(data.get("explainer"), str), "Explainer must be a string"
        return True
