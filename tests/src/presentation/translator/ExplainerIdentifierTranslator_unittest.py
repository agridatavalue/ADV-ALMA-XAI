import unittest

from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.presentation.translator.ExplainerIdentifierTranslator import (
    ExplainerIdentifierTranslator,
)


class TestExplainerIdentifierTranslator(unittest.TestCase):
    def setUp(self):
        self.testObj = ExplainerIdentifierTranslator()

    def test_translate(self):
        result = self.testObj.translate(
            {
                "data": "data",
                "model": "model",
                "prediction_target": "prediction_target",
            }
        )

        self.assertIsInstance(result, ExplainerIdentifier)
        self.assertEqual(result.data, "data")
        self.assertEqual(result.model, "model")
        self.assertEqual(result.prediction_target, "prediction_target")
