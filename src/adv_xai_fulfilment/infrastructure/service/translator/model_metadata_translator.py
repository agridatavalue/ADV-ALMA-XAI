from ....domain.model.model_metadata import ModelMetaData
from .feature_description_translator import FeatureDescriptionTranslator


class ModelMetaDataTranslator:
    _feature_translator: FeatureDescriptionTranslator

    def __init__(self) -> None:
        self._feature_translator = FeatureDescriptionTranslator()

    def translate(self, data: dict) -> ModelMetaData:
        return ModelMetaData(
            data_type=data.get("datatype", ""),
            algorithm=data.get("algorithm", "cnn"),
            framework=data.get("framework", "keras"),
            model_type=data.get("modeltype", ""),
            target_names=data.get("targetnames", ""),
            subject_name=data.get("Subjectname", ""),
            model_category=data.get("modelcategory", ""),
            feature_names=data.get("featurenames", ""),
            feature_descriptions=self._feature_translator.translate(
                data.get("feature_descriptions", {})
            ),
        )
