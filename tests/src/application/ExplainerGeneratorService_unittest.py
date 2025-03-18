import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.adv_xai_fulfilment.domain.model.model import Model
from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.service import ExplainerRetriever
from src.adv_xai_fulfilment.domain.model.model_data import ModelData
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.explainer import Explainer
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier

from src.adv_xai_fulfilment.application.ExplainerGeneratorService import (
    ExplainerGeneratorService,
)
from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    FeatureImportance,
)
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)
from src.adv_xai_fulfilment.infrastructure.service.ModelLoaderService import (
    ModelLoaderService,
)
from src.adv_xai_fulfilment.infrastructure.service.MetaDataLoaderService import (
    MetaDataLoaderService,
)
from src.adv_xai_fulfilment.domain.service.model_performance_service_component import (
    ModelPerformanceServiceComponent,
)
from src.adv_xai_fulfilment.infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)
from src.adv_xai_fulfilment.domain.service.feature_importance_service_component import (
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
            partner=Partner("test_partner"),
            model="test_model",
            metadata_identifier="test_metadata_identifier",
            prediction_target="target1",
        )

        # Mock model loader service
        mock_model = MagicMock(spec=Model)
        mock_model.name = "test"
        mock_model.is_ok.return_value = True
        mock_model.filename = "mock_model.pkl"

        model_data = ModelData()
        model_data.x = pd.DataFrame()
        model_data.y = pd.DataFrame()
        mock_data_loader_service = MagicMock(spec=DataLoaderService)
        mock_data_loader_service.load_data.return_value = model_data

        mock_model_loader_service = MagicMock(spec=ModelLoaderService)
        mock_model_loader_service.load_from.return_value = mock_model

        mock_metadata_loader_service = MagicMock(spec=MetaDataLoaderService)
        mock_metadata_loader_service.load_model_metadata.return_value = ModelMetaData(
            "tabular", "", "", "", "", "regression"
        )

        mock_mpm_service = MagicMock(spec=ModelPerformanceServiceComponent)
        mock_mpm_service.get_metrics.return_value = {"accuracy": 0.95}

        mock_feature_importance_service = MagicMock(
            spec=FeatureImportanceServiceComponent
        )
        mock_feature_importance_service.generate_data.return_value = FeatureImportance(
            importance=[0.5, 0.5],
            prediction_target="target1",
            feature=["feature1", "feature2"],
        )

        mock_explainer_retriever = MagicMock(spec=ExplainerRetriever)
        mock_explainer_retriever.get_by_data.return_value = [
            Explainer("test_explainer1", [], [], "", False, False, False, []),
            MyExplainer("test_explainer2", [], [], "", False, False, False, []),
        ]

        mock_explainer_service = MagicMock(spec=ExplainerRepositoryService)
        mock_explainer_service.upload_to.return_value = "/a/simple/path"

        # Instantiate the service
        service = ExplainerGeneratorService()
        service._mpm_service = mock_mpm_service
        service._explainer_service = mock_explainer_service
        service._data_loader_service = mock_data_loader_service
        service._explainer_retriever = mock_explainer_retriever
        service._model_loader_service = mock_model_loader_service
        service._fi_service_comp = mock_feature_importance_service
        service._metadata_loader_service = mock_metadata_loader_service

        result = service.generate_explainer(mock_identifier)

        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(x, Explainer) for x in result))
        self.assertEqual(len(result), 1)
