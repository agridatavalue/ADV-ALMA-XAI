from src.adv_xai_fulfilment.domain.model.explainers.responseData.FeatureDescription import (
    FeatureDescription,
)
from collections import Counter


class DataPresentationsOutputTranslator:
    def translate_data_source_types(
        self, descriptions: list[FeatureDescription]
    ) -> dict:
        type_counts = Counter(description.type for description in descriptions)

        return {
            "sources": [
                {"type": feature_type, "value": count}
                for feature_type, count in type_counts.items()
            ]
        }
