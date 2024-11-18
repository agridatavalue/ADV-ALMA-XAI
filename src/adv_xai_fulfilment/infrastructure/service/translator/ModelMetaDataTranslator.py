from ....domain.model.ModelMetaData import ModelMetaData
from ....domain.model.FeatureDescription import FeatureDescription


class ModelMetaDataTranslator:
    def translate_v2(self, data: dict) -> ModelMetaData:
        return ModelMetaData(
            data_type=data.get("datatype"),
            algorithm=data.get("algorithm", "cnn"),
            framework=data.get("framework", "keras"),
            model_type=data.get("modeltype"),
            target_names=data.get("targetnames"),
            model_category=data.get("modelcategory"),
            feature_names=data.get("featurenames"),
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
