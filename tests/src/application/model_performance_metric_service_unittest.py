import unittest
import pandas as pd
from unittest.mock import MagicMock, patch

from src.adv_xai_fulfilment.domain.model.model import Model
from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.model_data import ModelData
from src.adv_xai_fulfilment.domain.model.model_context import ModelContext
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.infrastructure.service.data_loader_service import DataLoaderService
from src.adv_xai_fulfilment.infrastructure.service.model_loader_service import ModelLoaderService
from src.adv_xai_fulfilment.infrastructure.service.metadata_loader_service import MetaDataLoaderService
from src.adv_xai_fulfilment.application.model_performance_metric_service import (
    ModelPerformanceMetricService,
)
from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    ModelPerformance,
)


class TestModelPerformanceMetricService(unittest.TestCase):
    @patch("os.getenv", return_value="mock/temp")
    @patch(
        "src.adv_xai_fulfilment.application.model_performance_metric_service.ModelPerformanceServiceComponent"
    )
    def test_get_data(
        self,
        MockMPMService,
        mock_getenv,
    ):
        mock_mpm_service = MockMPMService.return_value

        mock_model = MagicMock(spec=Model)
        mock_model_metadata = MagicMock(spec=ModelMetaData)
        explainer_identifier = ExplainerIdentifier(
            data="data",
            model="mock_model",
            partner=Partner("partner"),
            prediction_target="target",
            metadata_identifier="test_metadata_identifier",
        )

        mock_model_metadata.first_target_name = "default_target"
        mock_model_metadata.index_of_target_name.return_value = 0
        mock_model_metadata.feature_names = ["feature1", "feature2", "feature3"]
        mock_mpm_service.get_data.return_value = ModelPerformance(
            target="target", y_true=[], y_pred=[]
        )
        
        mock_model_data = MagicMock(spec=ModelData)
        mock_model_data.data_train = pd.DataFrame({
            "feature1": [1, 2, 3],
            "feature2": [4, 5, 6],
            "feature3": [7, 8, 9],
            "target": [0, 1, 0],
        })
        
        response = ModelContext(
            model=mock_model,
            model_data=mock_model_data,
            model_metadata=mock_model_metadata,
        )

        service = ModelPerformanceMetricService(
            data_loader_service = MagicMock(spec=DataLoaderService), 
            model_loader_service = MagicMock(spec=ModelLoaderService), 
            metadata_loader_service = MagicMock(spec=MetaDataLoaderService),        
        )
        service.get_context = MagicMock(return_value=response)
        
        result = service.get_data(explainer_identifier)

        self.assertIsInstance(result, ModelPerformance)
        self.assertEqual(result.target, "target")

    @patch("os.getenv", return_value="mock/temp")
    @patch(
        "src.adv_xai_fulfilment.application.model_performance_metric_service.ModelPerformanceServiceComponent"
    )
    def test_get_metrics(
        self,
        MockMPMService,
        mock_getenv,
    ):
        mock_mpm_service = MockMPMService.return_value

        mock_model = MagicMock(spec=Model)
        mock_model_metadata = MagicMock(spec=ModelMetaData)
        explainer_identifier = ExplainerIdentifier(
            data="crop",
            model="mock_model",
            partner=Partner("partner"),
            prediction_target="prediction_target",
            metadata_identifier="test_metadata_identifier",
        )

        mock_model_metadata.first_target_name = "default_target"
        mock_model_metadata.index_of_target_name.return_value = 1
        mock_mpm_service.get_metrics.return_value = {"precision": 0.85}
        
        mock_model_data = MagicMock(spec=ModelData)
        mock_model_data.data_train = pd.DataFrame({
            "feature1": [1, 2, 3],
            "feature2": [4, 5, 6],
            "feature3": [7, 8, 9],
            "target": [0, 1, 0],
        })
        
        response = ModelContext(
            model=mock_model,
            model_data=mock_model_data,
            model_metadata=mock_model_metadata,
        )

        service = ModelPerformanceMetricService(
            data_loader_service = MagicMock(spec=DataLoaderService), 
            model_loader_service = MagicMock(spec=ModelLoaderService), 
            metadata_loader_service = MagicMock(spec=MetaDataLoaderService), 
        )
        service.get_context = MagicMock(return_value=response)
        service._mdm_service = mock_mpm_service

        result = service.get_metrics(explainer_identifier)

        self.assertEqual(result["precision"], 0.85)
