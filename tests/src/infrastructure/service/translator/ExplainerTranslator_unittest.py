import unittest

from src.adv_xai_fulfilment.domain.model import ModelCategory
from src.adv_xai_fulfilment.domain.model.explainers import Explainer
from src.adv_xai_fulfilment.infrastructure.service.translator.ExplainerTranslator import (
    ExplainerTranslator,
)


class TestExplainerTranslator(unittest.TestCase):
    def setUp(self):
        self.testObj = ExplainerTranslator()

    def test_translate(self):
        result = self.testObj.translate(
            [
                {
                    "name": "name",
                    "type": ["type"],
                    "category": ["regression"],
                    "explanations": "explanations",
                    "is_distributed": True,
                    "train_set_required": True,
                    "has_categorical_features": True,
                    "data_type_explainers": ["data_type_explainers"],
                }
            ]
        )

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertTrue(all([isinstance(x, Explainer) for x in result]))
        self.assertEqual(result[0].name, "name")
        self.assertEqual(result[0].type, ["type"])
        self.assertEqual(result[0].category, ModelCategory.REGRESSION)
        self.assertEqual(result[0].explanations, "explanations")
        self.assertEqual(result[0].is_distributed, True)
        self.assertEqual(result[0].train_set_required, True)
        self.assertEqual(result[0].has_categorical_features, True)
        self.assertEqual(result[0].data_type_explainers, ["data_type_explainers"])
