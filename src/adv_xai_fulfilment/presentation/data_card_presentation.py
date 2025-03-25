import logging

from .validator import DataPresentationValidator
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..application.data_distribution_service import DataDistrubutionService
from ..application.feature_description_service import FeatureDescriptionService
from ..domain.model.explainers.response_data import FeatureDescription, DataDistribution
from .translator import ExplainerIdentifierTranslator, DataPresentationsOutputTranslator


class DataCardPresentations:
    _validator: DataPresentationValidator
    _input_translator: ExplainerIdentifierTranslator
    _output_translator: DataPresentationsOutputTranslator
    _data_distr_service: DataDistrubutionService
    _feature_description_service: FeatureDescriptionService

    def __init__(self):
        self._validator = DataPresentationValidator()
        self._input_translator = ExplainerIdentifierTranslator()
        self._output_translator = DataPresentationsOutputTranslator()
        self._feature_description_service = FeatureDescriptionService()
        self._data_distr_service = DataDistrubutionService()

    def get_data_distribution(self, request: dict = {}) -> DataDistribution:
        logging.info(f"called get_data_distribution with params: {request}")
        data_sanitized = self._validator.validate_and_sanitize_data_distribution(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._data_distr_service.get_data(expl_id)

    def get_data_source_types(self, request: dict = {}) -> dict:
        logging.info(f"called get_data_source_types with params: {request}")
        self._validator.validate_and_sanitize_data_source_types(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)

        descriptions: list[FeatureDescription] = (
            self._feature_description_service.get_data(expl_id)
        )
        return self._output_translator.translate_data_source_types(descriptions)

    