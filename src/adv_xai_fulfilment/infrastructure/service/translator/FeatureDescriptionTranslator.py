from src.adv_xai_fulfilment.domain.model.FeatureDescription import FeatureDescription


class FeatureDescriptionTranslator:
    def translate(self, data: dict = {}) -> list[FeatureDescription]:
        return [
            FeatureDescription(
                name=key,
                type=data[key].get("type") if type(data[key]) == dict else data[key],
                source=(
                    data[key].get("source") if type(data[key]) == dict else data[key]
                ),
                description=(
                    data[key].get("description")
                    if type(data[key]) == dict
                    else data[key]
                ),
            )
            for key in data.keys()
        ]
