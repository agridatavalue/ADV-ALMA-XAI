import unittest

from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.presentation.translator.ExplainerIdentifierTranslator import (
    RequestIdentifierTranslator,
)


class TestRequestIdentifierTranslator(unittest.TestCase):
    def setUp(self):
        self.testObj = RequestIdentifierTranslator()

    def test_translate(self):
        result = self.testObj.translate(
            {
                "data": "data",
                "model": "model",
                "meta_data": "meta_data",
                "prediction_target": "prediction_target",
            }
        )

        self.assertIsInstance(result, ExplainerIdentifier)
        self.assertEqual(result.data, "data")
        self.assertEqual(result.model, "model")
        self.assertEqual(result.metadata, "meta_data")
        self.assertEqual(result.prediction_target, "prediction_target")
