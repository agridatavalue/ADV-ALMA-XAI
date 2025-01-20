import logging

from ..domain.model.explainers.Explainer import Explainer
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..application.ExplainerGeneratorService import ExplainerGeneratorService
from .validator.ExplainerGeneratorValidator import ExplainerGeneratorValidator
from .translator.ExplainerIdentifierTranslator import ExplainerIdentifierTranslator


class ExplainerGeneratorPresentation:
    _validator: ExplainerGeneratorValidator
    _translator: ExplainerIdentifierTranslator
    _build_service: ExplainerGeneratorService

    def __init__(self):
        self._validator = ExplainerGeneratorValidator()
        self._translator = ExplainerIdentifierTranslator()
        self._build_service = ExplainerGeneratorService()

    def build(self, data: dict = {}) -> list[Explainer]:
        logging.info(f"called build with params: {data}")
        self._validator.validate_and_sanitize_build(data)
        requests: list[ExplainerIdentifier] = self._translator.translate_many(data)

        return [self._build_service.generate_explainer(request) for request in requests]

    def get_explainer_data(self, data: dict = {}):
        logging.info(f"called get_explainer_data with params: {data}")
        self._validator.validate_and_sanitize_get_data(data)
        return self._build_service.prepare_explainer(
            request=self._translator.translate(data),
            prediction_targets=data.get("prediction_targets", []),
        )

    def ask_to_explainer(self, data: dict = {}):
        logging.info(f"called ask_to_explainer with params: {data}")
        self._validator.validate_and_sanitize_ask(data)
        expl_id: ExplainerIdentifier = self._translator.translate(data)

        logging.info(f"Ask to Explainer: {str(expl_id)}")
        return self._build_service.ask_to_explainer(
            request=data.get("request"),
            explainer_name=data.get("explainer"),
            explainer_identifier=expl_id,
        )
