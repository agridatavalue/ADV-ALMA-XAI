import unittest

from src.adv_xai_fulfilment.domain.model.data_type import DataType
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers import Explainer
from src.adv_xai_fulfilment.domain.model.explainers.datatype_model_explainer import (
    DataTypeModelExplainer,
)


class TestExplainer(unittest.TestCase):
    def setUp(self):
        self.testObj = Explainer(
            name="name",
            type=["BlackBox"],
            categories=["Regression"],
            explanations="explanations",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TEXT, "explanations")
            ],
        )

    def test_set_meta_data(self):
        self.assertIsNone(self.testObj.meta_data)
        meta_data = ModelMetaData(
            data_type="Text",
            algorithm="algorithm",
            framework="framework",
            model_type="BlackBox",
            subject_name="subject_name",
            target_names=[],
            model_category="Regression",
            feature_descriptions=[],
        )
        self.testObj.set_meta_data(meta_data)
        self.assertEqual(self.testObj.meta_data, meta_data)

    def test_can_match_with(self):
        self.assertTrue(
            self.testObj.can_match_with(
                None,
                ModelMetaData(
                    data_type="Text",
                    algorithm="algorithm",
                    framework="framework",
                    model_type="BlackBox",
                    subject_name="subject_name",
                    target_names=[],
                    model_category="Regression",
                    feature_descriptions=[],
                ),
            )
        )

        self.assertFalse(
            self.testObj.can_match_with(
                None,
                {
                    "modeltype": "type",
                    "modelcategory": "category",
                    "datatype": "tabular",
                },
            )
        )
