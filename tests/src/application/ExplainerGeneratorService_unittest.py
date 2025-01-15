import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.adv_xai_fulfilment.domain.model.Model import Model
from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.domain.service.ExplainerRetriever import ExplainerRetriever
from src.adv_xai_fulfilment.application.ExplainerGeneratorService import (
    ExplainerGeneratorService,
)
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)
from src.adv_xai_fulfilment.infrastructure.service.ModelLoaderService import (
    ModelLoaderService,
)
from src.adv_xai_fulfilment.domain.service.ModelPerformanceServiceComponent import (
    ModelPerformanceServiceComponent,
)
from src.adv_xai_fulfilment.domain.service.FeatureImportanceServiceComponent import (
    FeatureImportanceServiceComponent,
)


class MyExplainer(Explainer):
    def build(self, model, data):
        self.build_result = True
        return self


class TestExplainerGeneratorService(unittest.TestCase):
    @patch("os.getenv", return_value="/mock/temp")
    def test_generate_explainer(self, mock_getenv):

        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            "DATA_FOLDER_PATH": "/data/folder",
            "EXPLAINER_FOLDER_PATH": "/explainer/folder",
            "MINIO_ENDPOINT": "test",
            "MINIO_ACCESS_KEY": "test",
            "MINIO_SECRET_KEY": "test",
            "MINIO_SECURE": "true",
        }.get(key, default)

        # Create a mock ExplainerIdentifier
        mock_identifier = ExplainerIdentifier(
            data="test_data",
            pilot=Pilot("test_pilot"),
            model="test_model",
            metadata=ModelMetaData("", "", "", "", "", ""),
            prediction_target="target1",
        )

        # Mock model loader service
        mock_model = MagicMock(spec=Model)
        mock_model.filename = "mock_model.pkl"

        mock_data_loader_service = MagicMock(spec=DataLoaderService)
        mock_data_loader_service.load_data.return_value = {
            "train": pd.DataFrame(),
            "test": pd.DataFrame(),
        }

        mock_model_loader_service = MagicMock(spec=ModelLoaderService)
        mock_model_loader_service.load_from.return_value = mock_model

        mock_mpm_service = MagicMock(spec=ModelPerformanceServiceComponent)
        mock_mpm_service.get_metrics.return_value = {"accuracy": 0.95}

        mock_feature_importance_service = MagicMock(
            spec=FeatureImportanceServiceComponent
        )
        mock_feature_importance_service.generate_data.return_value = {
            "Feature": ["feature1", "feature2"],
            "Importance": [0.5, 0.5],
            "prediction_target": "target1",
        }

        mock_explainer_retriever = MagicMock(spec=ExplainerRetriever)
        mock_explainer_retriever.get_by_data.return_value = [
            Explainer("test_explainer1", [], [], "", False, False, False, []),
            MyExplainer("test_explainer2", [], [], "", False, False, False, []),
        ]

        # Instantiate the service
        service = ExplainerGeneratorService()
        service._mpm_service = mock_mpm_service
        service._data_loader_service = mock_data_loader_service
        service._explainer_retriever = mock_explainer_retriever
        service._model_loader_service = mock_model_loader_service
        service._fi_service_comp = mock_feature_importance_service

        result = service.generate_explainer(
            mock_identifier, prediction_targets=["target1"]
        )

        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(x, Explainer) for x in result))
        self.assertEqual(len(result), 1)
