from .FeedbackTranslator import FeedbackTranslator
from .ExplainerTranslator import ExplainerTranslator
from .ModelMetaDataTranslator import ModelMetaDataTranslator
from src.adv_xai_fulfilment.domain.model import ExplainerMetaData
from .FeatureImportanceTranslator import FeatureImportanceTranslator
from .FeatureDescriptionTranslator import FeatureDescriptionTranslator
from .ModelPerformanceMetricsTranslator import ModelPerformanceMetricsTranslator


class ExplainerMetaDataTranslator:
    _feedback_translator: FeedbackTranslator
    _explainer_translator: ExplainerTranslator
    _model_metadata_translator: ModelMetaDataTranslator
    _feature_importance_translator: FeatureImportanceTranslator
    _feature_description_translator: FeatureDescriptionTranslator
    _model_performance_metrics_translator: ModelPerformanceMetricsTranslator

    def __init__(self):
        self._feedback_translator = FeedbackTranslator()
        self._explainer_translator = ExplainerTranslator()
        self.model_metadata_translator = ModelMetaDataTranslator()
        self._feature_importance_translator = FeatureImportanceTranslator()
        self._feature_description_translator = FeatureDescriptionTranslator()
        self._model_performance_metrics_translator = ModelPerformanceMetricsTranslator()

    def translate(self, metadata: dict) -> ExplainerMetaData:
        model_metadata = metadata.get("model_metadata", {})
        return ExplainerMetaData(
            target_name=model_metadata.get("targetname", ""),
            meta_data=self.model_metadata_translator.translate(
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
