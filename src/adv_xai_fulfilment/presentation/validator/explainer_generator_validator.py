from .abstract_validator import AbstractValidator
from src.adv_xai_fulfilment.infrastructure.constants import Errors


class ExplainerGeneratorValidator(AbstractValidator):
    def validate_and_sanitize_build(self, data: dict) -> dict:
        self._validate_model(data.get("model", ""))
        self._validate_partner(data.get("partner", ""))
        
        if not isinstance(data.get("data_for_train"), str):
            raise TypeError(Errors.DATA_FOR_TRAIN_FOLDER_NOT_STRING)
        if not isinstance(data.get("data_for_predict"), str):
            raise TypeError(Errors.DATA_FOR_PREDICT_FOLDER_NOT_STRING)
        return data

    def validate_and_sanitize_ask(self, data: dict) -> dict:
        self._validate_partner(data.get("partner", ""))
        if not isinstance(data.get("request"), str):
            raise TypeError("Request must be a string")
        if not isinstance(data.get("explainer"), str):
            raise TypeError("Explainer must be a string")
        return data

    def validate_and_sanitize_get_data(self, data: dict) -> dict:
        self._validate_model(data.get("model", ""))
        self._validate_partner(data.get("partner", ""))
        return data
