import unittest

from src.adv_xai_fulfilment.domain.model.explainers.responseData import (
    FeatureDescription,
)
from src.adv_xai_fulfilment.infrastructure.service.translator.FeatureDescriptionTranslator import (
    FeatureDescriptionTranslator,
)


class TestFeatureDescriptionTranslator(unittest.TestCase):
    def setUp(self):
        self.testObj = FeatureDescriptionTranslator()

    def test_translate_feature_descriptions(self):
        result = self.testObj.translate(
            {
                "Row distance (cm)": {
                    "description": "Distance between plantation rows in cm",
                    "source": "field measurement",
                    "type": "agronomic",
                },
                "NO3-N 0-30 cm start (kg/ha)": {
                    "description": "Nitrate content in the soil at 0-30 cm depth at the start of the season",
                    "source": "agronomic",
                    "type": "soil",
                },
            }
        )

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all([isinstance(fd, FeatureDescription) for fd in result]))
        self.assertEqual(result[0].name, "Row distance (cm)")
        self.assertEqual(result[0].type, "agronomic")
        self.assertEqual(result[0].source, "field measurement")
        self.assertEqual(
            result[0].description, "Distance between plantation rows in cm"
        )
