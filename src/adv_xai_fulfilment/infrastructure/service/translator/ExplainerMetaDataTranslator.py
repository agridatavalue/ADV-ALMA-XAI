from .FeedbackTranslator import FeedbackTranslator
from .ExplainerTranslator import ExplainerTranslator
from .ModelMetaDataTranslator import ModelMetaDataTranslator
from .FeatureDescriptionTranslator import FeatureDescriptionTranslator
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData


class ExplainerMetaDataTranslator:
    _feedback_translator: FeedbackTranslator
    _explainer_translator: ExplainerTranslator
    _model_metadata_translator: ModelMetaDataTranslator
    _feature_description_translator: FeatureDescriptionTranslator

    def __init__(self):
        self._feedback_translator = FeedbackTranslator()
        self._explainer_translator = ExplainerTranslator()
        self.model_metadata_translator = ModelMetaDataTranslator()
        self._feature_description_translator = FeatureDescriptionTranslator()

    def translate(self, metadata: dict) -> ExplainerMetaData:
        model_metadata = metadata.get("model_metadata", {})
        return ExplainerMetaData(
            metrics=metadata.get("metrics", {}),
            target_name=model_metadata.get("targetname", ""),
            meta_data=self.model_metadata_translator.translate(
                metadata.get("meta_data", {})
            ),
            possible_explainers=self._explainer_translator.translate(
                metadata.get("possible_explainers", [])
            ),
            feature_importance=model_metadata.get("feature_importance", {}),
            feedback=self._feedback_translator.translate_many(
                metadata.get("feedback_and_improvements", [])
            ),
        )
