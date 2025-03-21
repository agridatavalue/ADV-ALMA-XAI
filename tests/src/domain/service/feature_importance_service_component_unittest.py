import unittest
from unittest.mock import MagicMock

from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.explainer import Explainer
from src.adv_xai_fulfilment.domain.model.explainer_metadata import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    FeatureImportance,
)
from src.adv_xai_fulfilment.infrastructure.service.MetaDataLoaderService import (
    MetaDataLoaderService,
)
from src.adv_xai_fulfilment.domain.service.feature_importance_service_component import (
    FeatureImportanceServiceComponent,
)


class TestFeatureImportanceServiceComponent(unittest.TestCase):

    def setUp(self):
        self.request = ExplainerIdentifier(
            model="test",
            partner=Partner("test"),
            prediction_target="test",
            metadata_identifier="test",
        )

    def test_get_data(self):
        mock_metadata_loader_service = MagicMock(spec=MetaDataLoaderService)
        mock_metadata_loader_service.load_explainer_metadata.return_value = (
            ExplainerMetaData(
                metrics={},
                meta_data=ModelMetaData,
                target_name="target",
                possible_explainers=[
                    Explainer(
                        "name",
                        type=[],
                        categories=[],
                        explanations="",
                        is_distributed=False,
                        train_set_required=False,
                        has_categorical_features=False,
                        data_type_explainers=[],
                    )
                ],
                feature_importance=FeatureImportance(
                    feature=["feature1"], importance=[0.1], prediction_target="target"
                ),
            )
        )

        testObj = FeatureImportanceServiceComponent()
        testObj._metadata_loader_service = mock_metadata_loader_service

        actual = testObj.get_data(self.request)

        self.assertIsInstance(actual, FeatureImportance)
        self.assertEqual(actual.feature, ["feature1"])
        self.assertEqual(actual.importance, [0.1])
        self.assertEqual(actual.prediction_target, "target")

    @unittest.skip("Not implemented")
    def test_generate_data(self):
        testObj = FeatureImportanceServiceComponent()
        testObj.generate_data(self.request)
