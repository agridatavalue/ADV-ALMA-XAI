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
        
    def test_is_classification(self):
        self.assertTrue(ModelCategory.is_classification("CLASSIFICATION"))
        self.assertFalse(ModelCategory.is_classification("REGRESSION"))
        
    def test_is_regression(self):
        self.assertTrue(ModelCategory.is_regression("REGRESSION"))
        self.assertFalse(ModelCategory.is_regression("CLASSIFICATION"))
