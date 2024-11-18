import unittest

from src.adv_xai_fulfilment.domain.model.DataType import DataType
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.domain.model.explainers.DataTypeModelExplainer import (
    DataTypeModelExplainer,
)


class TestExplainer(unittest.TestCase):
    def setUp(self):
        self.testObj = Explainer(
            name="name",
            type=["BlackBox"],
            category=["Regression"],
            explanations="explanations",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TEXT, "explanations")
            ],
        )

    def test_can_match_with(self):
        self.assertTrue(
            self.testObj.can_match_with(
                None,
                ModelMetaData(
                    data_type="Text",
                    algorithm="algorithm",
                    framework="framework",
                    model_type="BlackBox",
                    targetnames=[],
                    model_category="Regression",
                    feature_descriptions=[],
                ),
            )
        )

    def test_can_match_with_not_matching(self):
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
