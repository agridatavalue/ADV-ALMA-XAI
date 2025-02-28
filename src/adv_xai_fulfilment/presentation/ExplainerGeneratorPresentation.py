import logging

from .validator import ExplainerGeneratorValidator
from .translator import ExplainerIdentifierTranslator
from ..domain.model.explainers.explainer import Explainer
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import ExplainerResponseData
from ..application.explainer_generator_service import ExplainerGeneratorService


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

        explainers: list[list[Explainer]] = [
            self._build_service.generate_explainer(request) for request in requests
        ]
        return sum(explainers, [])

    def prepare(self, data: dict = {}) -> bool:
        logging.info(f"called prepare with params: {data}")
        self._validator.validate_and_sanitize_prepare(data)
        requests: list[ExplainerIdentifier] = self._translator.translate_many(data)

        for request in requests:
            self._build_service.prepare_explainer(request)

        return True

    def get_explainer_guide(self, data: dict = {}) -> list[ExplainerResponseData]:
        logging.info(f"called get_explainer_data with params: {data}")
        self._validator.validate_and_sanitize_get_data(data)
        expl_id: ExplainerIdentifier = self._translator.translate(data)
        return self._build_service.describe_explainer(request=expl_id)

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
