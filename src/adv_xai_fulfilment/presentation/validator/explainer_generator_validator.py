import os

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
    
        return {
            **data,
            "data_for_train": self.__handle_path_and_url( data.get("data_for_train", "")),
            "data_for_predict": self.__handle_path_and_url( data.get("data_for_predict", "")), 
        }

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
        return self._merge_with_default_values(data)
    
    def validate_and_sanitize_get_summary(self, data: dict) -> dict:
        self._validate_model(data.get("model", ""))
        self._validate_partner(data.get("partner", ""))
        return {**self._merge_with_default_values(data), "language": data.get("language", "en")}
    
    def __handle_path_and_url(self, path: str) -> str:
        if not path: 
            return ''
    
        validated_path = path
        if path.startswith("http://") or path.startswith("https://"):
            validated_path = path.split(f"{os.getenv('STORE_ENDPOINT')}/{os.getenv('EXPLAINER_FOLDER_PATH')}/")[-1]

        return validated_path if validated_path[-1] != "/" else validated_path[:-1]
