import unittest
from unittest.mock import MagicMock

from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.domain.service.FeatureImportanceServiceComponent import (
    FeatureImportanceServiceComponent,
)


class TestFeatureImportanceServiceComponent(unittest.TestCase):

    def setUp(self):
        self.request = ExplainerIdentifier(
            model="test", metadata="test", prediction_target="test", pilot=Pilot("test")
        )

    def test_get_data(self):
        testObj = FeatureImportanceServiceComponent()
        testObj._data_loader_service.load_explainer_metadata = MagicMock(
            return_value=ExplainerMetaData(
                metrics={},
                meta_data=ModelMetaData,
                target_name="target",
                possible_explainers=[
                    Explainer(
                        "name",
                        type=[],
                        category=[],
                        explanations="",
                        is_distributed=False,
                        train_set_required=False,
                        has_categorical_features=False,
                        data_type_explainers=[],
                    )
                ],
                feature_importance={
                    "Feature": ["feature1"],
                    "Importance": [0.1],
                    "prediction_target": "target",
                },
            )
        )
        actual = testObj.get_data(self.request)

        self.assertEqual(
            actual,
            {
                "Feature": ["feature1"],
                "Importance": [0.1],
                "prediction_target": "target",
            },
        )

    @unittest.skip("Not implemented")
    def test_generate_data(self):
        testObj = FeatureImportanceServiceComponent()
        testObj.generate_data(self.request)
