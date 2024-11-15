import unittest

from src.adv_xai_fulfilment.domain.model.FeatureDescription import FeatureDescription
from src.adv_xai_fulfilment.application.translator.FeatureDescriptionTranslator import (
    FeatureDescriptionTranslator,
)


class TestFeatureDescriptionTranslator(unittest.TestCase):
    def setUp(self):
        self.testObj = FeatureDescriptionTranslator()

    def test_translate(self):
        result = self.testObj.translate(
            key="Row distance (cm)",
            data={
                "description": "Distance between plantation rows in cm",
                "source": "field measurement",
                "type": "agronomic",
            },
        )

        self.assertIsInstance(result, FeatureDescription)
        self.assertEqual(result.name, "Row distance (cm)")
        self.assertEqual(result.type, "agronomic")
        self.assertEqual(result.source, "field measurement")
        self.assertEqual(result.description, "Distance between plantation rows in cm")
