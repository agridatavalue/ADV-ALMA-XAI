from logger import get_logger

from .validator import DataPresentationValidator
from ..application.targets_service import TargetsService
from ..domain.model.explainers.response_data import Targets
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..application.data_distribution_service import DataDistrubutionService
from ..application.feature_description_service import FeatureDescriptionService
from ..domain.model.explainers.response_data import FeatureDescription, DataDistribution
from .translator import ExplainerIdentifierTranslator, DataPresentationsOutputTranslator

logger = get_logger()

class DataCardPresentations:
    _validator: DataPresentationValidator
    _targets_service: TargetsService
    _input_translator: ExplainerIdentifierTranslator
    _output_translator: DataPresentationsOutputTranslator
    _data_distr_service: DataDistrubutionService
    _feature_description_service: FeatureDescriptionService

    def __init__(self):
        self._targets_service = TargetsService()
        self._validator = DataPresentationValidator()
        self._data_distr_service = DataDistrubutionService()
        self._input_translator = ExplainerIdentifierTranslator()
        self._output_translator = DataPresentationsOutputTranslator()
        self._feature_description_service = FeatureDescriptionService()

    def get_targets(self, request: dict = {}) -> Targets:
        logger.info(f"called get_targets with params: {request}")
        self._validator.validate_and_sanitize_targets(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)
        return self._targets_service.get_data(expl_id)

    def get_data_distribution(self, request: dict = {}) -> DataDistribution:
        logger.info(f"called get_data_distribution with params: {request}")
        data_sanitized = self._validator.validate_and_sanitize_data_distribution(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._data_distr_service.get_data(expl_id, data_sanitized.get('bin_size'))

    def get_data_source_types(self, request: dict = {}) -> dict:
        logger.info(f"called get_data_source_types with params: {request}")
        self._validator.validate_and_sanitize_data_source_types(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)

        descriptions: list[FeatureDescription] = (
            self._feature_description_service.get_data(expl_id)
        )
        return self._output_translator.translate_data_source_types(descriptions)

    