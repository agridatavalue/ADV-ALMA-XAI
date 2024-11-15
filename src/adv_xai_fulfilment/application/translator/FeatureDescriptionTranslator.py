from ...domain.model.FeatureDescription import FeatureDescription


class FeatureDescriptionTranslator:
    def translate(self, key: str, data: dict) -> FeatureDescription:
        return FeatureDescription(
            name=key,
            type=data["type"],
            source=data["source"],
            description=data["description"],
        )
