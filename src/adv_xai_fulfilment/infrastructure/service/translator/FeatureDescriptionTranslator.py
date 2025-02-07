from src.adv_xai_fulfilment.domain.model.explainers.responseData import (
    FeatureDescription,
)


class FeatureDescriptionTranslator:
    def translate(self, data: dict = {}) -> list[FeatureDescription]:
        return [
            FeatureDescription(
                name=key,
                type=(
                    data[key].get("type") if isinstance(data[key], dict) else data[key]
                ),
                source=(
                    data[key].get("source")
                    if isinstance(data[key], dict)
                    else data[key]
                ),
                description=(
                    data[key].get("description")
                    if isinstance(data[key], dict)
                    else data[key]
                ),
            )
            for key in data.keys()
        ]
