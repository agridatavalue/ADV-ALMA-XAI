from src.adv_xai_fulfilment.domain.model.FeatureDescription import FeatureDescription


class FeatureDescriptionTranslator:
    def translate(self, data: dict = {}) -> list[FeatureDescription]:
        return [
            FeatureDescription(
                name=key,
                type=data[key].get("type"),
                source=data[key].get("source"),
                description=data[key].get("description"),
            )
            for key in data.keys()
        ]
