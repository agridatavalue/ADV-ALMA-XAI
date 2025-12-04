from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    FeatureDescription, DataSourceTypes
)


class DataPresentationsOutputTranslator:
    def translate_data_source_types(
        self, descriptions: list[FeatureDescription]
    ) -> DataSourceTypes:
        data = DataSourceTypes()
        for feature in descriptions:
            data.add_source_type(feature.type, 1)
        return data
