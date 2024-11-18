import unittest

from src.adv_xai_fulfilment.domain.model.DataType import DataType


class TestDataType(unittest.TestCase):

    def test_from_string(self):
        self.assertEqual(DataType.from_string("text"), DataType.TEXT)
        self.assertEqual(DataType.from_string("Text"), DataType.TEXT)
        self.assertEqual(DataType.from_string("TEXT"), DataType.TEXT)
        self.assertEqual(DataType.from_string("image"), DataType.IMAGE)
        self.assertEqual(DataType.from_string("Image"), DataType.IMAGE)
        self.assertEqual(DataType.from_string("IMAGE"), DataType.IMAGE)
        self.assertEqual(DataType.from_string("tabular"), DataType.TABULAR)
        self.assertEqual(DataType.from_string("Tabular"), DataType.TABULAR)
        self.assertEqual(DataType.from_string("TABULAR"), DataType.TABULAR)
        self.assertIsNone(DataType.from_string("UNKNOWN"))
        self.assertIsNone(DataType.from_string(""))

    def test_values(self):
        self.assertEqual(DataType.TEXT, "TEXT")
        self.assertEqual(DataType.IMAGE, "IMAGE")
        self.assertEqual(DataType.TABULAR, "TABULAR")
