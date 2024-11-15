import logging

from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from .validator.ExplainerGeneratorValidator import ExplainerGeneratorValidator
from ..application.ExplainerGeneratorService import ExplainerGeneratorService
from .translator.ExplainerIdentifierTranslator import ExplainerIdentifierTranslator


class ExplainerGeneratorPresentation:
    _service: ExplainerGeneratorService
    _validator: ExplainerGeneratorValidator
    _translator: ExplainerIdentifierTranslator

    def __init__(self):
        self._service = ExplainerGeneratorService()
        self._validator = ExplainerGeneratorValidator()
        self._translator = ExplainerIdentifierTranslator()

    def build(self, data: dict):
        self._validator.validate_build(data)
        request: ExplainerIdentifier = self._translator.translate(data)

        logging.info(
            f"Building Explainer with modelName: {request.model}, pilot: {request.pilot}"
        )
        return self._service.generate_explainer(
            request, data.get("prediction_targets", [])
        )

    def ask_to_explainer(self, data: dict):
        self._validator.validate_ask(data)
        expl_id: ExplainerIdentifier = self._translator.translate(data)

        logging.info(
            f"Ask to Explainer with pilot: {expl_id.pilot}, request: {data.get('request')}, explainer: {data.get('explainer')}"
        )
        return self._service.ask_to_explainer(
            request=data.get("request"),
            explainer_name=data.get("explainer"),
            explainer_identifier=expl_id,
        )
