import unittest
from unittest.mock import MagicMock

from src.adv_xai_fulfilment.domain.model.pilot import Pilot
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.application.FeatureImportanceService import (
    FeatureImportanceService,
)
from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    FeatureImportance,
)
from src.adv_xai_fulfilment.domain.service.feature_importance_service_component import (
    FeatureImportanceServiceComponent,
)


class TestFeatureImportanceService(unittest.TestCase):
    def test_get_data(self):
        mock_fi_service = MagicMock(spec=FeatureImportanceServiceComponent)
        mock_fi_service.get_data.return_value = FeatureImportance("test")

        testObj = FeatureImportanceService()
        testObj._feature_importance_service_comp = mock_fi_service

        actual = testObj.get_data(
            ExplainerIdentifier(
                model="model",
                pilot=Pilot("pilot"),
                metadata_identifier="metadata_identifier",
                prediction_target="prediction_target",
            )
        )

        self.assertIsInstance(actual, FeatureImportance)
