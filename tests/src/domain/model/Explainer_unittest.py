import unittest

from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.domain.model.explainers.DataTypeModel import DataTypeModel
from src.adv_xai_fulfilment.domain.model.explainers.DataTypeModelExplainer import (
    DataTypeModelExplainer,
)


class TestExplainer(unittest.TestCase):
    def setUp(self):
        self.testObj = Explainer(
            name="name",
            type=["type"],
            category=["category"],
            explanations="explanations",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataTypeModel.TEXT, "explanations")
            ],
        )

    def test_can_match_with(self):
        self.assertTrue(
            self.testObj.can_match_with(
                None,
                {
                    "modeltype": "type",
                    "modelcategory": "category",
                    "datatype": DataTypeModel.TEXT,
                },
            )
        )

    def test_can_match_with_not_matching(self):
        self.assertFalse(
            self.testObj.can_match_with(
                None,
                {
                    "modeltype": "type",
                    "modelcategory": "category",
                    "datatype": DataTypeModel.TABULAR,
                },
            )
        )
