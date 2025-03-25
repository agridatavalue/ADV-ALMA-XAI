import os
import logging

from .validator import DataPresentationValidator
from ..application.heatmap_service import HeatmapService
from ..domain.model.explainers.response_data import Heatmap
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import ConfusionMatrix
from ..domain.model.explainers.response_data import FeatureImportance
from ..domain.model.explainers.response_data import FeatureDescription
from ..application.confusion_matrix_service import ConfusionMatrixService
from ..domain.model.explainers.response_data import ModelPerformanceMetrics
from ..application.feature_importance_service import FeatureImportanceService
from ..application.partial_dependence_service import PartialDependenceService
from ..application.feature_description_service import FeatureDescriptionService
from ..domain.model.explainers.response_data import IndividualConditionalExpectations
from ..application.model_performance_metric_service import ModelPerformanceMetricService
from .translator import ExplainerIdentifierTranslator, DataPresentationsOutputTranslator
from ..application.data_features_average_score_service import DataFeaturesAverageScoreService
from ..application.individual_conditional_expectations_service import IndividualConditionalExpectationService
from ..domain.model.explainers.response_data import ModelPerformance, PartialDependence, DataFeaturesAndAverageScore
from ..application.plot_scatter_observed_predicted_service import (
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
    _heatmap_service: HeatmapService
    _dfas_service: DataFeaturesAverageScoreService
    _ice_service: IndividualConditionalExpectationService

    _validator: DataPresentationValidator

    def __init__(self):
        self._validator = DataPresentationValidator()
        self._heatmap_service = HeatmapService()
        self._dfas_service = DataFeaturesAverageScoreService()
        self._input_translator = ExplainerIdentifierTranslator()
        self._output_translator = DataPresentationsOutputTranslator()
        self._plot_scatter_service = PlotScatterObservedPredictedService()
        self._confusion_matrix_service = ConfusionMatrixService()
        self._model_performance_service = ModelPerformanceMetricService()
        self._feature_importance_service = FeatureImportanceService()
        self._partial_dependence_service = PartialDependenceService()
        self._feature_description_service = FeatureDescriptionService()
        self._ice_service = IndividualConditionalExpectationService()

    def get_data_features_and_average_score(self, request: dict = {}) -> DataFeaturesAndAverageScore:
        logging.info(f"called get_data_features_and_average_score with params: {request}")
        data_sanitized = self._validator.validate_and_sanitize_data_features_and_average_score(
            request
        )
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._dfas_service.get_data(expl_id)

    def get_individual_conditional_expectations(self, request: dict = {}) -> IndividualConditionalExpectations:
        logging.info(f"called get_individual_conditional_expectations with params: {request}")
        data_sanitized = self._validator.validate_and_sanitize_individual_conditional_expectations(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)

        return self._ice_service.get_data(expl_id, data_sanitized.get("feature"))

    def get_image(self, request: dict = {}) -> str:
        logging.info(f"called get_image with params: {request}")
        self._validator.validate_and_sanitize_get_image(request)

        complete_filepath: str = os.path.join(
            os.getenv("TEMP"), request.get("filename")
        )
        if complete_filepath == request.get("filename"):
            complete_filepath = os.getenv("TEMP") + request.get("filename")

        if not os.path.exists(complete_filepath):
            raise FileNotFoundError(f"File not found: {request.get('filename')}")

        return complete_filepath

    def get_heatmap(self, request: dict = {}) -> Heatmap:
        logging.info(f"called get_heatmap with params: {request}")
        self._validator.validate_and_sanitize_heatmap(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)
        return self._heatmap_service.get_data(expl_id)

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
        return self._plot_scatter_service.genarate_data_for_partner(expl_id)

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

        return self._partial_dependence_service.get_data(expl_id, data_sanitized.get("feature"))

    def get_confusion_matrix(self, data: dict = {}) -> ConfusionMatrix:
        logging.info(f"called get_confusion_matrix with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_confusion_matrix(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._confusion_matrix_service.get_data(expl_id)
