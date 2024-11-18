import unittest

from src.adv_xai_fulfilment.domain.model.explainers.DataTypeModel import DataTypeModel


class TestDataTypeModel(unittest.TestCase):

    def test_from_string(self):
        self.assertEqual(DataTypeModel.from_string("text"), DataTypeModel.TEXT)
        self.assertEqual(DataTypeModel.from_string("Text"), DataTypeModel.TEXT)
        self.assertEqual(DataTypeModel.from_string("TEXT"), DataTypeModel.TEXT)
        self.assertEqual(DataTypeModel.from_string("image"), DataTypeModel.IMAGE)
        self.assertEqual(DataTypeModel.from_string("Image"), DataTypeModel.IMAGE)
        self.assertEqual(DataTypeModel.from_string("IMAGE"), DataTypeModel.IMAGE)
        self.assertEqual(DataTypeModel.from_string("tabular"), DataTypeModel.TABULAR)
        self.assertEqual(DataTypeModel.from_string("Tabular"), DataTypeModel.TABULAR)
        self.assertEqual(DataTypeModel.from_string("TABULAR"), DataTypeModel.TABULAR)
        self.assertIsNone(DataTypeModel.from_string("UNKNOWN"))
        self.assertIsNone(DataTypeModel.from_string(""))

    def test_values(self):
        self.assertEqual(DataTypeModel.TEXT, "TEXT")
        self.assertEqual(DataTypeModel.IMAGE, "IMAGE")
        self.assertEqual(DataTypeModel.TABULAR, "TABULAR")
