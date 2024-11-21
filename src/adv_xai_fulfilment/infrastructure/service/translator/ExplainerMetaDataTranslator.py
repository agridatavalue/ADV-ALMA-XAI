from .ExplainerTranslator import ExplainerTranslator
from .ModelMetaDataTranslator import ModelMetaDataTranslator
from .FeatureDescriptionTranslator import FeatureDescriptionTranslator
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData


class ExplainerMetaDataTranslator:
    _explainer_translator: ExplainerTranslator
    _model_metadata_translator: ModelMetaDataTranslator
    _feature_description_translator: FeatureDescriptionTranslator

    def __init__(self):
        self._explainer_translator = ExplainerTranslator()
        self.model_metadata_translator = ModelMetaDataTranslator()
        self._feature_description_translator = FeatureDescriptionTranslator()

    def translate(self, metadata: dict) -> ExplainerMetaData:
        return ExplainerMetaData(
            metrics=metadata.get("metrics", {}),
            target_name=metadata.get("target_name", {}),
            meta_data=self.model_metadata_translator.translate(
                metadata.get("meta_data", {})
            ),
            possible_explainers=self._explainer_translator.translate(
                metadata.get("possible_explainers", [])
            ),
            feature_importance=metadata.get("feature_importance", {}),
        )
