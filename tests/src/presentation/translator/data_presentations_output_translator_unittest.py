import unittest

from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    FeatureDescription,
)
from src.adv_xai_fulfilment.presentation.translator import (
    DataPresentationsOutputTranslator,
)


class TestDataPresentationsOutputTranslator(unittest.TestCase):
    def test_translate_data_source_types(self):
        # Given
        descriptions = [
            FeatureDescription(
                "feature1", type="type1", source="source1", description="description1"
            ),
            FeatureDescription(
                "feature2", type="type1", source="source1", description="description1"
            ),
            FeatureDescription(
                "feature3", type="type2", source="source1", description="description1"
            ),
            FeatureDescription(
                "feature4", type="type2", source="source1", description="description1"
            ),
            FeatureDescription(
                "feature5", type="type3", source="source1", description="description1"
            ),
        ]
        translator = DataPresentationsOutputTranslator()

        # When
        result = translator.translate_data_source_types(descriptions)

        # Then
        self.assertEqual(
            result,
            {
                "sources": [
                    {"type": "type1", "value": 2},
                    {"type": "type2", "value": 2},
                    {"type": "type3", "value": 1},
                ]
            },
        )
