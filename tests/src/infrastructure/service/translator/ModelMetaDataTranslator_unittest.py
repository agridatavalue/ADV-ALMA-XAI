import unittest

from src.adv_xai_fulfilment.domain.model.DataType import DataType
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.infrastructure.service.translator.ModelMetaDataTranslator import (
    ModelMetaDataTranslator,
)


class TestModelMetaDataTranslator(unittest.TestCase):
    def setUp(self):
        self.testObj = ModelMetaDataTranslator()

    def test_translate(self):
        result = self.testObj.translate(
            {
                "datatype": "tabular",
                "framework": "framework",
                "algorithm": "algorithm",
                "targetnames": ["targetnames"],
                "modelcategory": "modelcategory",
            }
        )

        self.assertIsInstance(result, ModelMetaData)
        self.assertEqual(result.data_type, DataType.TABULAR)
        self.assertEqual(result.framework, "framework")
        self.assertEqual(result.algorithm, "algorithm")
        self.assertEqual(result.target_names, ["targetnames"])
        self.assertEqual(result.model_category, "modelcategory")
