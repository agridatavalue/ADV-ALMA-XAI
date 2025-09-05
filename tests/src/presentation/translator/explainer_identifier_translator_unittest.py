import unittest

from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.presentation.translator import ExplainerIdentifierTranslator


class TestExplainerIdentifierTranslator(unittest.TestCase):
    def setUp(self):
        self.testObj = ExplainerIdentifierTranslator()

    def test_translate(self):
        result = self.testObj.translate(
            {
                "model": "model",
                "data_for_predict": "data",
                "prediction_target": "prediction_target",
            }
        )

        self.assertIsInstance(result, ExplainerIdentifier)
        self.assertEqual(result.data, "data")
        self.assertEqual(result.model, "model")
        self.assertEqual(result.prediction_target, "prediction_target")

    def test_translate_many_without_target(self):
        result = self.testObj.translate_many(
            {
                "data_for_predict": "data",
                "model": "model",
            }
        )

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertTrue(all(isinstance(r, ExplainerIdentifier) for r in result))
        self.assertEqual(result[0].data, "data")
        self.assertEqual(result[0].model, "model")

    def test_translate_many_with_multiple_targets(self):
        result = self.testObj.translate_many(
            {
                "model": "model",
                "data_for_predict": "data",
                "prediction_targets": [
                    "prediction_target_1",
                    "prediction_target_2",
                ],
            }
        )

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(r, ExplainerIdentifier) for r in result))
        self.assertEqual(result[0].data, "data")
        self.assertEqual(result[0].model, "model")
        self.assertEqual(result[0].prediction_target, "prediction_target_1")
        self.assertEqual(result[1].data, "data")
        self.assertEqual(result[1].model, "model")
        self.assertEqual(result[1].prediction_target, "prediction_target_2")
