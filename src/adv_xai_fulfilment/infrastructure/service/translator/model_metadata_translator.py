from typing import Optional

from ....domain.model.model_metadata import ModelMetaData
from ....domain.model.model_metadata_layer import ModelMetaDataLayer
from .feature_description_translator import FeatureDescriptionTranslator

class ModelMetaDataTranslator:
    _feature_translator: FeatureDescriptionTranslator

    def __init__(self):
        self._feature_translator = FeatureDescriptionTranslator()
        
    def _translate_architectures(self, data: list[dict]) -> list[ModelMetaDataLayer]:
        return [
            ModelMetaDataLayer.create(
                type=item.get("type", ""),
                parameters=item.get("parameters", {}),
            )
            for item in data if isinstance(item, dict) and item.get("type") 
        ]
        
    def _translate_n_classes(self, data) -> Optional[int]:
        if isinstance(data, int):
            return data
        if isinstance(data, str) and data.isdigit():
            return int(data)
        return None
    
    def _translate_input_shape(self, data) -> list[int]:
        if not isinstance(data, list):
            return []
        
        if all(isinstance(i, int) for i in data):
            return data
        
        if all(isinstance(i, str) and i.isdigit() for i in data):
            return [int(i) for i in data]
        
        return []

    def translate(self, data: dict) -> ModelMetaData:
        architectures = data.get('architectures', {})
        return ModelMetaData(
            n_classes=self._translate_n_classes(architectures.get("n_classes")),
            data_type=data.get("datatype", ""),
            algorithm=data.get("algorithm", "cnn"),
            framework=data.get("framework", "torch"),
            model_type=data.get("modeltype", ""),
            input_shape=self._translate_input_shape(architectures.get("input_shape", [])),
            target_names=data.get("targetnames", ""),
            subject_name=data.get("Subjectname", ""),
            model_category=data.get("modelcategory", ""),
            feature_names=data.get("featurenames", ""),
            architectures=self._translate_architectures(architectures.get("layers", [])),
            feature_descriptions=self._feature_translator.translate(
                data.get("feature_descriptions", {})
            ),
        )