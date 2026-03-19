from logger import get_logger
from ..domain.model.partner import Partner
from .validator import ExplainerGeneratorValidator
from .translator import ExplainerIdentifierTranslator
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainer_guide import ExplainerGuide
from ..domain.model.explainers.explainer import Explainer
from ..domain.model.explainers.response_data import ModelSummary
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..application.explainer_generator_service import ExplainerGeneratorService
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService
from ..application.model_summary_explanation_service import ModelSummaryExplanationService

logger = get_logger()

class ExplainerGeneratorPresentation:
    _validator: ExplainerGeneratorValidator
    _translator: ExplainerIdentifierTranslator
    _build_service: ExplainerGeneratorService
    _summary_service: ModelSummaryExplanationService
    _metadata_loader_service: MetaDataLoaderService

    def __init__(self):
        self._validator = ExplainerGeneratorValidator()
        self._translator = ExplainerIdentifierTranslator()
        self._build_service = ExplainerGeneratorService()
        self._metadata_loader_service = MetaDataLoaderService()
        self._summary_service = ModelSummaryExplanationService()

    def build(self, data: dict = {}) -> list[Explainer]:
        logger.info(f"called build with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_build(data)

        if not data_sanitized.get('prediction_targets'):
            model_metadata: ModelMetaData = self._metadata_loader_service.load_model_metadata(
                expl_id=ExplainerIdentifier(
                    prediction_target = "",
                    data = data.get("data_for_predict", ""),
                    model = data.get("model", ""),
                    partner = Partner(data.get("partner", "")),
                    metadata_identifier = data.get("metadata", data.get("meta_data", "")),
                )
            )
            logger.debug(f"setting {model_metadata.target_names} as prediction_targets")
            data['prediction_targets'] = model_metadata.target_names

        requests: list[ExplainerIdentifier] = self._translator.translate_many(data_sanitized)

        explainers: list[list[Explainer]] = [
            self._build_service.generate_explainer(request) for request in requests
        ]
        return sum(explainers, [])

    def get_explainer_guide(self, data: dict = {}) -> ExplainerGuide:
        logger.info(f"called get_explainer_data with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_get_data(data)
        expl_id: ExplainerIdentifier = self._translator.translate(data_sanitized)
        return self._build_service.describe_explainer(request=expl_id)
    
    def get_model_summary(self, data: dict = {}) -> ModelSummary:
        logger.info(f"called get_model_summary with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_get_summary(data)
        expl_id: ExplainerIdentifier = self._translator.translate(data_sanitized)

        logger.info(f"Get Model Summary for: {str(expl_id)}")
        return self._summary_service.get_model_summary(
            explainer_identifier=expl_id,
            language=data_sanitized.get("language", 'en')
        )