import os

from logger import get_logger
from .validator import DataPresentationValidator
from .translator import ExplainerIdentifierTranslator
from ..domain.model.explainer_identifier import ExplainerIdentifier

logger = get_logger()


class HelpersPresentation:
    _validator: DataPresentationValidator
    _input_translator: ExplainerIdentifierTranslator

    def __init__(self):
        self._validator = DataPresentationValidator()
        self._input_translator = ExplainerIdentifierTranslator()

    def get_image(self, request: dict = {}) -> str:
        logger.info(f"called get_image with params: {request}")
        data_sanitized: dict = self._validator.validate_and_sanitize_get_image(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)

        complete_filepath: str = expl_id.get_data_locale_filepath(data_sanitized.get("filename"))
        if not os.path.exists(complete_filepath):
            raise FileNotFoundError(f"File not found: {request.get('filename')}")

        return complete_filepath