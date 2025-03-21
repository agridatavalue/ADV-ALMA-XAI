import unittest

from src.adv_xai_fulfilment.domain.model.model_category import ModelCategory


class TestModelCategory(unittest.TestCase):
    def test_from_string(self):
        self.assertEqual(
            ModelCategory.from_string("Classification"), ModelCategory.CLASSIFICATION
        )
        self.assertEqual(
            ModelCategory.from_string("REGRESSION"), ModelCategory.REGRESSION
        )
        self.assertRaises(ValueError, ModelCategory.from_string, "unknown")
