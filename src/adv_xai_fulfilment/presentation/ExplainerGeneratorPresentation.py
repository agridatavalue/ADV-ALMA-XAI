import logging

from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from .validator.ExplainerGeneratorValidator import ExplainerGeneratorValidator
from ..application.ExplainerGeneratorService import ExplainerGeneratorService
from .translator.ExplainerIdentifierTranslator import ExplainerIdentifierTranslator


class ExplainerGeneratorPresentation:
    _validator: ExplainerGeneratorValidator
    _translator: ExplainerIdentifierTranslator
    _build_service: ExplainerGeneratorService

    def __init__(self):
        self._validator = ExplainerGeneratorValidator()
        self._translator = ExplainerIdentifierTranslator()
        self._build_service = ExplainerGeneratorService()

    def build(self, data: dict):
        self._validator.validate_and_sanitize_build(data)
        request: ExplainerIdentifier = self._translator.translate(data)

        logging.info(
            f"Building Explainer with modelName: {request.model}, pilot: {request.pilot}"
        )
        return self._build_service.generate_explainer(
            request, data.get("prediction_targets", [])
        )

    def ask_to_explainer(self, data: dict):
        self._validator.validate_and_sanitize_ask(data)
        expl_id: ExplainerIdentifier = self._translator.translate(data)

        logging.info(
            f"Ask to Explainer with pilot: {expl_id.pilot}, request: {data.get('request')}, explainer: {data.get('explainer')}"
        )
        return self._build_service.ask_to_explainer(
            request=data.get("request"),
            explainer_name=data.get("explainer"),
            explainer_identifier=expl_id,
        )
