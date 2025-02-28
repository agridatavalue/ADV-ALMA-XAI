from .heatmap_translator import HeatmapTranslator
from .feedback_translator import FeedbackTranslator
from .explainer_translator import ExplainerTranslator
from .model_metadata_translator import ModelMetaDataTranslator
from .feature_importance_translator import FeatureImportanceTranslator
from .feature_description_translator import FeatureDescriptionTranslator
from .model_performance_metrics_translator import ModelPerformanceMetricsTranslator
from src.adv_xai_fulfilment.domain.model.explainer_metadata import ExplainerMetaData


class ExplainerMetaDataTranslator:
    _heatmap_translator: HeatmapTranslator
    _feedback_translator: FeedbackTranslator
    _explainer_translator: ExplainerTranslator
    _model_metadata_translator: ModelMetaDataTranslator
    _feature_importance_translator: FeatureImportanceTranslator
    _feature_description_translator: FeatureDescriptionTranslator
    _model_performance_metrics_translator: ModelPerformanceMetricsTranslator

    def __init__(self):
        self._heatmap_translator = HeatmapTranslator()
        self._feedback_translator = FeedbackTranslator()
        self._explainer_translator = ExplainerTranslator()
        self._model_metadata_translator = ModelMetaDataTranslator()
        self._feature_importance_translator = FeatureImportanceTranslator()
        self._feature_description_translator = FeatureDescriptionTranslator()
        self._model_performance_metrics_translator = ModelPerformanceMetricsTranslator()

    def translate(self, metadata: dict) -> ExplainerMetaData:
        model_metadata = metadata.get("model_metadata", {})
        explainer_metadata = metadata.get("explainer_metadata", {})

        return ExplainerMetaData(
            target_name=model_metadata.get("targetname", ""),
            heatmap_images=self._heatmap_translator.translate(
                explainer_metadata.get("heatmaps", [])
            ),
            meta_data=self._model_metadata_translator.translate(
                metadata.get("meta_data", {})
            ),
            feedback=self._feedback_translator.translate_many(
                metadata.get("feedback_and_improvements", [])
            ),
            possible_explainers=self._explainer_translator.translate(
                metadata.get("possible_explainers", [])
            ),
            metrics=self._model_performance_metrics_translator.translate(
                model_metadata.get("performance_metrics", {})
            ),
            feature_importance=self._feature_importance_translator.translate(
                model_metadata.get("feature_importance", {})
            ),
        )
