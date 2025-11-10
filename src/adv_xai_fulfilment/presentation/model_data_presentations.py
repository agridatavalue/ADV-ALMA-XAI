from logger import get_logger
from .validator import DataPresentationValidator
from ..application.heatmap_service import HeatmapService
from ..application.lift_curve_service import LiftCurveService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..application.anomaly_score_service import AnomalyScoreService
from ..application.feature_impact_service import FeatureImpactService
from ..application.confusion_matrix_service import ConfusionMatrixService
from ..application.class_label_sizes_service import ClassLabelSizesService
from ..domain.model.explainers.response_data import ModelPerformanceMetrics
from ..domain.model.explainers.response_data import Heatmap, ClassLabelSizes
from ..application.feature_importance_service import FeatureImportanceService
from ..application.partial_dependence_service import PartialDependenceService
from ..domain.model.explainers.response_data import ConfusionMatrix, LiftCurve
from ..application.feature_description_service import FeatureDescriptionService
from ..domain.model.explainers.response_data import FeatureImportance, AnomalyScore
from ..domain.model.explainers.response_data import FeatureDescription, FeatureImpact
from ..domain.model.explainers.response_data import IndividualConditionalExpectations
from ..application.model_performance_metric_service import ModelPerformanceMetricService
from .translator import ExplainerIdentifierTranslator, DataPresentationsOutputTranslator
from ..application.data_features_average_score_service import DataFeaturesAverageScoreService
from ..application.individual_conditional_expectations_service import IndividualConditionalExpectationService
from ..domain.model.explainers.response_data import ModelPerformance, PartialDependence, DataFeaturesAndAverageScore
from ..application.plot_scatter_observed_predicted_service import (
    PlotScatterObservedPredictedService,
)

logger = get_logger()

class ModelDataPresentations:
    _feature_importance_service: FeatureImportanceService
    _feature_description_service: FeatureDescriptionService
    _partial_dependence_service: PartialDependenceService
    _model_performance_service: ModelPerformanceMetricService
    _confusion_matrix_service: ConfusionMatrixService
    _feature_impact_service: FeatureImpactService
    _anomaly_scores_service: AnomalyScoreService
    _plot_scatter_service: PlotScatterObservedPredictedService
    _output_translator: DataPresentationsOutputTranslator
    _input_translator: ExplainerIdentifierTranslator
    _heatmap_service: HeatmapService
    _dfas_service: DataFeaturesAverageScoreService
    _ice_service: IndividualConditionalExpectationService
    _lift_curve_service = LiftCurveService
    _cls_service: ClassLabelSizesService

    _validator: DataPresentationValidator

    def __init__(self):
        self._validator = DataPresentationValidator()
        self._heatmap_service = HeatmapService()
        self._cls_service = ClassLabelSizesService()
        self._dfas_service = DataFeaturesAverageScoreService()
        self._input_translator = ExplainerIdentifierTranslator()
        self._output_translator = DataPresentationsOutputTranslator()
        self._plot_scatter_service = PlotScatterObservedPredictedService()
        self._confusion_matrix_service = ConfusionMatrixService()
        self._model_performance_service = ModelPerformanceMetricService()
        self._feature_importance_service = FeatureImportanceService()
        self._partial_dependence_service = PartialDependenceService()
        self._feature_description_service = FeatureDescriptionService()
        self._feature_impact_service = FeatureImpactService()
        self._ice_service = IndividualConditionalExpectationService()
        self._anomaly_scores_service = AnomalyScoreService()
        self._lift_curve_service = LiftCurveService()

    def get_lift_curve(self, request: dict = {}) -> LiftCurve:
        logger.info(f"called get_lift_curve with params: {request}")
        data_sanitized = self._validator.validate_and_sanitize_lift_curve(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._lift_curve_service.get_data(expl_id=expl_id)

    def get_class_label_sizes(self, request: dict = {}) -> ClassLabelSizes:
        logger.info(f"called get_class_label_sizes with params: {request}")
        data_sanitized = self._validator.validate_and_sanitize_class_label_sizes(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._cls_service.get_data(expl_id)

    def get_data_features_and_average_score(self, request: dict = {}) -> DataFeaturesAndAverageScore:
        logger.info(f"called get_data_features_and_average_score with params: {request}")
        data_sanitized = self._validator.validate_and_sanitize_data_features_and_average_score(
            request
        )
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._dfas_service.get_data(expl_id)

    def get_individual_conditional_expectations(self, request: dict = {}) -> IndividualConditionalExpectations:
        logger.info(f"called get_individual_conditional_expectations with params: {request}")
        data_sanitized = self._validator.validate_and_sanitize_individual_conditional_expectations(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)

        return self._ice_service.get_data(expl_id, data_sanitized.get("feature", ""))

    def get_heatmap(self, request: dict = {}) -> Heatmap:
        logger.info(f"called get_heatmap with params: {request}")
        self._validator.validate_and_sanitize_heatmap(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)
        return self._heatmap_service.get_data(expl_id)

    def get_feature_description(self, request: dict = {}) -> list[FeatureDescription]:
        logger.info(f"called get_feature_description with params: {request}")
        self._validator.validate_and_sanitize_feature_description(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)

        return self._feature_description_service.get_data(expl_id)

    def get_feature_importance(self, request: dict = {}) -> FeatureImportance:
        logger.info(f"called get_feature_importance with params: {request}")
        self._validator.validate_and_sanitize_feature_importance(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)

        return self._feature_importance_service.get_data(expl_id)
    
    def get_feature_impact(self, request: dict = {}) -> FeatureImpact:
        logger.info(f"called get_feature_impact with params: {request}")
        self._validator.validate_and_sanitize_feature_impact(request)
        expl_id: ExplainerIdentifier = self._input_translator.translate(request)
        return self._feature_impact_service.get_data(expl_id, requested_feature=request.get("feature", ""))

    def genarate_performance_scatter_plot(self, data: dict = {}) -> dict:
        data_sanitized: dict = self._validator.validate_and_sanitize_scatter(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._plot_scatter_service.genarate_data_for_partner(expl_id)

    def get_model_performance_metrics(self, data: dict = {}) -> ModelPerformanceMetrics:
        logger.info(f"called get_model_performance_metrics with params: {data}")
        data_sanitized: dict = (
            self._validator.validate_and_sanitize_model_performance_metrics(data)
        )
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)

        return self._model_performance_service.get_metrics(expl_id)

    def genarate_model_performance(self, data: dict = {}) -> ModelPerformance:
        logger.info(f"called genarate_model_performance with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_model_performance(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)

        return self._model_performance_service.get_data(expl_id)

    def get_partial_dependence(self, data: dict = {}) -> PartialDependence:
        logger.info(f"called get_partial_dependence with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_partial_dependence(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)

        return self._partial_dependence_service.get_data(expl_id, data_sanitized.get("feature", ""))

    def get_confusion_matrix(self, data: dict = {}) -> ConfusionMatrix:
        logger.info(f"called get_confusion_matrix with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_confusion_matrix(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._confusion_matrix_service.get_data(expl_id)

    def get_anomaly_score(self, data: dict = {}) -> AnomalyScore:
        logger.info(f"called get_anomaly_score with params: {data}")
        data_sanitized = self._validator.validate_and_sanitize_anomaly_score(data)
        expl_id: ExplainerIdentifier = self._input_translator.translate(data_sanitized)
        return self._anomaly_scores_service.get_data(expl_id)