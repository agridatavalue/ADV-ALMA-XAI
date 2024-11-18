from ....domain.model.ModelMetaData import ModelMetaData
from ....domain.model.FeatureDescription import FeatureDescription


class ModelMetaDataTranslator:
    def translate_v2(self, data: dict) -> ModelMetaData:
        return ModelMetaData(
            data_type=data.get("data_type"),
            algorithm=data.get("algorithm", "cnn"),
            framework=data.get("framework", "keras"),
            targetnames=data.get("targetnames"),
            model_category=data.get("modelcategory"),
            feature_descriptions=[
                FeatureDescription(
                    name=feature.get("name"),
                    type=feature.get("type"),
                    source=feature.get("source"),
                    description=feature.get("description"),
                )
                for feature in data.get("feature_descriptions")
            ],
        )
