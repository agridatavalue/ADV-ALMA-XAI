from logger import get_logger
from ..domain.model.partner import Partner
from .validator import ExplainerGeneratorValidator
from .translator import ExplainerIdentifierTranslator
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainers.explainer import Explainer
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import ExplainerResponseData
from ..application.explainer_generator_service import ExplainerGeneratorService
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService

logger = get_logger()

class ExplainerGeneratorPresentation:
    _validator: ExplainerGeneratorValidator
    _translator: ExplainerIdentifierTranslator
    _build_service: ExplainerGeneratorService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._validator = ExplainerGeneratorValidator()
        self._translator = ExplainerIdentifierTranslator()
        self._build_service = ExplainerGeneratorService()
        self._metadata_loader_service = MetaDataLoaderService()

    def build(self, data: dict = {}) -> list[Explainer]:
        logger.info(f"called build with params: {data}")
        self._validator.validate_and_sanitize_build(data)

        if not data.get('prediction_targets'):
            model_metadata: ModelMetaData = self._metadata_loader_service.load_model_metadata(
                expl_id=ExplainerIdentifier(
                    prediction_target = "",
                    data = data.get("data_for_predict", ""),
                    model = data.get("model", ""),
                    partner = Partner(data.get("partner", "")),
                    metadata_identifier = data.get("meta_data", ""),
                )
            )
            logger.debug(f"setting {model_metadata.target_names} as prediction_targets")
            data['prediction_targets'] = model_metadata.target_names

        requests: list[ExplainerIdentifier] = self._translator.translate_many(data)

        explainers: list[list[Explainer]] = [
            self._build_service.generate_explainer(request) for request in requests
        ]
        return sum(explainers, [])

    def get_explainer_guide(self, data: dict = {}) -> list[ExplainerResponseData]:
        logger.info(f"called get_explainer_data with params: {data}")
        self._validator.validate_and_sanitize_get_data(data)
        expl_id: ExplainerIdentifier = self._translator.translate(data)
        return self._build_service.describe_explainer(request=expl_id)

    def ask_to_explainer(self, data: dict = {}):
        logger.info(f"called ask_to_explainer with params: {data}")
        self._validator.validate_and_sanitize_ask(data)
        expl_id: ExplainerIdentifier = self._translator.translate(data)

        logger.info(f"Ask to Explainer: {str(expl_id)}")
        return self._build_service.ask_to_explainer(
            request=data.get("request", ""),
            explainer_name=data.get("explainer", ""),
            explainer_identifier=expl_id,
        )
