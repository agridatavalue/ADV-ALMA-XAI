import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.adv_xai_fulfilment.domain.model.Model import Model
from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.application.ExplainerGeneratorService import (
    ExplainerGeneratorService,
)


class TestExplainerGeneratorService(unittest.TestCase):
    @patch(
        "src.adv_xai_fulfilment.application.ExplainerGeneratorService.DataLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ExplainerGeneratorService.ModelLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ExplainerGeneratorService.ExplainerRetriever"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ExplainerGeneratorService.ModelPerformanceMetricServiceComponent"
    )
    @patch("os.getenv")
    def test_generate_explainer(
        self,
        mock_getenv,
        mock_mpm_service,
        mock_explainer_retriever,
        mock_model_loader_service,
        mock_data_loader_service,
    ):
        # Mock environment variables
        mock_getenv.side_effect = lambda key: {
            "DATA_FOLDER_PATH": "/data/folder",
            "EXPLAINER_FOLDER_PATH": "/explainer/folder",
        }.get(key, None)

        # Create a mock ExplainerIdentifier
        mock_identifier = ExplainerIdentifier(
            data="test_data",
            pilot="test_pilot",
            model="test_model",
            metadata="test_metadata",
            prediction_target="target1",
        )

        # Mock model loader service
        mock_model = MagicMock(spec=Model)
        mock_model.filename = "mock_model.pkl"
        mock_model_loader_service.return_value.load_from.return_value = mock_model

        # Mock data loader service
        mock_data_loader_service.return_value.load_meta_data.return_value = {
            "targetnames": ["target1", "target2"],
            "modelcategory": "classification",
        }
        mock_data_loader_service.return_value.load_data.return_value = {
            "train": pd.DataFrame(),
            "test": pd.DataFrame(),
        }

        # Mock explainer retriever
        mock_explainer = MagicMock(spec=Explainer)
        mock_explainer.name = "mock_explainer"
        mock_explainer_retriever.return_value.get_by_data.return_value = [
            mock_explainer
        ]

        # Mock performance metric service
        mock_mpm_service.return_value.get_metrics.return_value = {"accuracy": 0.95}

        # Instantiate the service
        service = ExplainerGeneratorService()

        prediction_targets = ["target1"]
        result = service.generate_explainer(mock_identifier, prediction_targets)

        self.assertIsInstance(result, list)
        self.assertIsInstance(all(isinstance(x, Explainer) for x in result), bool)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "mock_explainer")


if __name__ == "__main__":
    unittest.main()
