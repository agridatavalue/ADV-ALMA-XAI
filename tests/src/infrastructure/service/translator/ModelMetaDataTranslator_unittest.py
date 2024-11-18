import unittest

from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.FeatureDescription import FeatureDescription
from src.adv_xai_fulfilment.infrastructure.service.translator.ModelMetaDataTranslator import (
    ModelMetaDataTranslator,
)


class TestModelMetaDataTranslator(unittest.TestCase):
    def setUp(self):
        self.testObj = ModelMetaDataTranslator()

    def test_translate_v2(self):
        result = self.testObj.translate_v2(
            {
                "datatype": "data_type",
                "framework": "framework",
                "algorithm": "algorithm",
                "targetnames": ["targetnames"],
                "modelcategory": "modelcategory",
                "feature_descriptions": [
                    {
                        "name": "name",
                        "data_type": "data_type",
                        "description": "description",
                    }
                ],
            }
        )

        self.assertIsInstance(result, ModelMetaData)
        self.assertEqual(result.data_type, "data_type")
        self.assertEqual(result.framework, "framework")
        self.assertEqual(result.algorithm, "algorithm")
        self.assertEqual(result.target_names, ["targetnames"])
        self.assertEqual(result.model_category, "modelcategory")
        self.assertIsInstance(result.feature_descriptions, list)
        self.assertTrue(
            all(
                [
                    isinstance(fd, FeatureDescription)
                    for fd in result.feature_descriptions
                ]
            )
        )
