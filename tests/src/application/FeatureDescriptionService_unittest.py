import unittest
from unittest.mock import MagicMock

from src.adv_xai_fulfilment.domain.model import Pilot, ExplainerIdentifier
from src.adv_xai_fulfilment.application.FeatureDescriptionService import (
    FeatureDescriptionService,
)
from src.adv_xai_fulfilment.domain.service.FeatureDescriptionServiceComponent import (
    FeatureDescriptionServiceComponent,
)
from src.adv_xai_fulfilment.domain.model.explainers.responseData import (
    FeatureDescription,
)


class TestFeatureDescriptionService(unittest.TestCase):
    def test_get_data(self):
        mock_feature_d_service = MagicMock(spec=FeatureDescriptionServiceComponent)
        mock_feature_d_service.get_data.return_value = [FeatureDescription()]

        feature_description_service = FeatureDescriptionService()
        feature_description_service._feature_description_service = (
            mock_feature_d_service
        )

        actual = feature_description_service.get_data(
            explainer_identifier=ExplainerIdentifier(
                model="model",
                pilot=Pilot("pilot"),
                metadata_identifier="metadata_v2.json",
                prediction_target="prediction_target",
            )
        )
        self.assertIsInstance(actual, list)
        self.assertTrue(len(actual) > 0)
        self.assertTrue(all(isinstance(x, FeatureDescription) for x in actual))
