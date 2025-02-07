import logging

from ..domain.model import ExplainerIdentifier
from ..domain.model.explainers.responseData import ConfusionMatrix
from ..domain.model.explainers.responseData import ModelPerformanceMetrics
from ..application.ConfusionMatrixService import ConfusionMatrixService
from .validator.DataPresentationValidator import DataPresentationValidator
from ..application.FeatureImportanceService import FeatureImportanceService
from ..application.PartialDependenceService import PartialDependenceService
from ..application.FeatureDescriptionService import FeatureDescriptionService
from .translator.ExplainerIdentifierTranslator import ExplainerIdentifierTranslator
from ..application.ModelPerformanceMetricService import ModelPerformanceMetricService
from ..domain.model.explainers.responseData import PartialDependence, FeatureImportance
from ..domain.model.explainers.responseData import FeatureDescription, ModelPerformance
from .translator.DataPresentationsOutputTranslator import (
    DataPresentationsOutputTranslator,
)
from ..application.PlotScatterObservedPredictedService import (
    PlotScatterObservedPredictedService,
)


class DataPresentations:
    _feature_importance_service: FeatureImportanceService
    _feature_description_service: FeatureDescriptionService
    _partial_dependence_service: PartialDependenceService
    _model_performance_service: ModelPerformanceMetricService
    _confusion_matrix_service: ConfusionMatrixService
    _plot_scatter_service: PlotScatterObservedPredictedService
    _output_translator: DataPresentationsOutputTranslator
    _input_translator: ExplainerIdentifierTranslator
    _validator: DataPresentationValidator

    def __init__(self):
        self._validator = DataPresentationValidator()
        self._input_translator = ExplainerIdentifierTranslator()
        self._output_translator = DataPresentationsOutputTranslator()
        self._plot_scatter_service = PlotScatterObservedPredictedService()
        self._confusion_matrix_service = ConfusionMatrixService()
        self._model_performance_service = ModelPerformanceMetricService()
        self._feature_importance_service = FeatureImportanceService()
        self._partial_dependence_service = PartialDependenceService()
        self._feature_description_service = FeatureDescriptionService()

    def get_data_source_types(self, request: dict = {}) -> dict:
        logging.info(f"called get_data_source_types with params: {request}")
        self._validator.validate_and_sanitize_data_source_types(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)

        descriptions: list[FeatureDescription] = (
            self._feature_description_service.get_data(expl_id)
        )
        return self._output_translator.translate_data_source_types(descriptions)

    def get_feature_description(self, request: dict = {}) -> list[FeatureDescription]:
        logging.info(f"called get_feature_description with params: {request}")
        self._validator.validate_and_sanitize_feature_description(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)

        return self._feature_description_service.get_data(expl_id)

    def get_feature_importance(self, request: dict = {}) -> FeatureImportance:
        logging.info(f"called get_feature_importance with params: {request}")
        self._validator.validate_and_sanitize_feature_importance(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)

        return self._feature_importance_service.get_data(expl_id)

    def genarate_performance_scatter_plot(self, data: dict = {}) -> dict:
        data_sanitized: dict = self._validator.validate_and_sanitize_scatter(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._plot_scatter_service.genarate_data_for_pilot(expl_id)

    def get_model_performance_metrics(self, data: dict = {}) -> ModelPerformanceMetrics:
        logging.info(f"called get_model_performance_metrics with params: {data}")
        data_sanitized: dict = (
            self._validator.validate_and_sanitize_model_performance_metrics(data)
        )
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)

        return self._model_performance_service.get_metrics(expl_id)

    def genarate_model_performance(self, data: dict = {}) -> ModelPerformance:
        logging.info(f"called genarate_model_performance with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_model_performance(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)

        return self._model_performance_service.get_data(expl_id)

    def get_partial_dependence(self, data: dict = {}) -> PartialDependence:
        logging.info(f"called get_partial_dependence with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_partial_dependence(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)

        return self._partial_dependence_service.get_data(
            expl_id, data_sanitized.get("feature")
        )

    def get_confusion_matrix(self, data: dict = {}) -> ConfusionMatrix:
        logging.info(f"called get_confusion_matrix with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_confusion_matrix(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._confusion_matrix_service.get_data(expl_id)
