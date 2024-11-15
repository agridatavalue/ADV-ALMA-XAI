from ..infrastructure.Constants import Errors
from ..application.PlotScatterObservedPredictedService import (
    PlotScatterObservedPredictedService,
)
from ..domain.model.FeatureDescription import FeatureDescription
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from .validator.DataPresentationValidator import DataPresentationValidator
from ..application.FeatureImportanceService import FeatureImportanceService
from .translator.ExplainerIdentifierTranslator import ExplainerIdentifierTranslator
from ..application.ModelPerformanceMetricService import ModelPerformanceMetricService


class DataPresentations:
    _feature_importance_service: FeatureImportanceService
    _model_performance_service: ModelPerformanceMetricService
    _plot_scatter_service: PlotScatterObservedPredictedService
    _translator: ExplainerIdentifierTranslator
    _validator: DataPresentationValidator

    def __init__(self):
        self._validator = DataPresentationValidator()
        self._translator = ExplainerIdentifierTranslator()
        self._plot_scatter_service = PlotScatterObservedPredictedService()
        self._model_performance_service = ModelPerformanceMetricService()
        self._feature_importance_service = FeatureImportanceService()

    def genarate_feature_description(
        self, request: dict = {}
    ) -> list[FeatureDescription]:
        self._validator.validate_feature_description(request)
        expl_id: ExplainerIdentifier = self._translator.translate(request)

        return self._feature_importance_service.genarate_feature_description(expl_id)

    def genarate_feature_importance(
        self, request: dict = {}
    ) -> dict[
        "Feature" : list[str],
        "Importance" : list[float],
        "prediction_target":str,
    ]:
        self._validator.validate_feature_importance(request)
        expl_id: ExplainerIdentifier = self._translator.translate(request)

        return self._feature_importance_service.get_data(expl_id)

    def genarate_performance_scatter_plot(self, model_file_name: str) -> dict:
        assert isinstance(model_file_name, str), Errors.MODEL_FILENAME_NOT_STRING
        return self._plot_scatter_service.genarate_data_for_pilot(model_file_name)

    def get_model_performance_metric(
        self, model_filename: str, prediction_target: int
    ) -> dict:
        assert isinstance(model_filename, str), Errors.MODEL_FILENAME_NOT_STRING
        assert isinstance(
            prediction_target, int
        ), Errors.PREDICTION_TARGET_INDEX_NOT_INT

        return self._model_performance_service.get_metrics(
            model_filename=model_filename, prediction_target=prediction_target
        )

    def genarate_model_performance(self, model_file_name: str) -> dict:
        assert isinstance(model_file_name, str), Errors.MODEL_FILENAME_NOT_STRING
        return self._model_performance_service.get_data(model_filename=model_file_name)
