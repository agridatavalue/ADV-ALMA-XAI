import os
import unittest
from unittest.mock import MagicMock, patch

from src.adv_xai_fulfilment.domain.model.Model import Model
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.application.ModelPerformanceMetricService import (
    ModelPerformanceMetricService,
)


class TestModelPerformanceMetricService(unittest.TestCase):
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.DataLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.ModelLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.ModelPerformanceMetricServiceComponent"
    )
    def test_get_data(self, MockMPMService, MockModelLoader, MockDataLoader):
        # Mock dependencies
        mock_data_loader = MockDataLoader.return_value
        mock_model_loader = MockModelLoader.return_value
        mock_mpm_service = MockMPMService.return_value

        # Mock objects
        mock_model = MagicMock(spec=Model)
        mock_model_metadata = MagicMock(spec=ModelMetaData)
        explainer_identifier = ExplainerIdentifier(
            data="data",
            pilot="pilot",
            model="mock_model",
            metadata="metadata",
            prediction_target="target",
        )

        # Mock returns
        mock_model_loader.load_from.return_value = mock_model
        mock_data_loader.load_data.return_value = {"mock_key": "mock_value"}
        mock_data_loader.load_model_metadata.return_value = mock_model_metadata
        mock_model_metadata.first_target_name = "default_target"
        mock_model_metadata.index_of_target_name.return_value = 0
        mock_mpm_service.get_data.return_value = {"accuracy": 0.95}

        # Instantiate service
        service = ModelPerformanceMetricService()

        # Call method
        result = service.get_data(explainer_identifier)

        # Assertions
        mock_model_loader.load_from.assert_called_once_with(explainer_identifier.model)
        mock_data_loader.load_data.assert_called_once_with(
            bucket_name=os.getenv("DATA_FOLDER_PATH"),
            folder_path=explainer_identifier.data,
        )
        mock_data_loader.load_model_metadata.assert_called_once_with(
            explainer_identifier
        )
        mock_mpm_service.get_data.assert_called_once_with(
            data={"mock_key": "mock_value"},
            model=mock_model,
            prediction_target_index=0,
        )

        self.assertEqual(result["accuracy"], 0.95)
        self.assertEqual(result["target"], "target")

    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.DataLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.ModelLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.ModelPerformanceMetricServiceComponent"
    )
    def test_get_metrics(self, MockMPMService, MockModelLoader, MockDataLoader):
        # Mock dependencies
        mock_data_loader = MockDataLoader.return_value
        mock_model_loader = MockModelLoader.return_value
        mock_mpm_service = MockMPMService.return_value

        # Mock objects
        mock_model = MagicMock(spec=Model)
        mock_model_metadata = MagicMock(spec=ModelMetaData)
        explainer_identifier = ExplainerIdentifier(
            data="crop",
            pilot="pilot",
            model="mock_model",
            metadata="metadata",
            prediction_target="prediction_target",
        )

        # Mock returns
        mock_model_loader.load_from.return_value = mock_model
        mock_data_loader.load_data.return_value = {"mock_key": "mock_value"}
        mock_data_loader.load_model_metadata.return_value = mock_model_metadata
        mock_model_metadata.first_target_name = "default_target"
        mock_model_metadata.index_of_target_name.return_value = 1
        mock_mpm_service.get_metrics.return_value = {"precision": 0.85}

        # Instantiate service
        service = ModelPerformanceMetricService()

        # Call method
        result = service.get_metrics(explainer_identifier)

        # Assertions
        mock_model_loader.load_from.assert_called_once_with(explainer_identifier.model)
        mock_data_loader.load_data.assert_called_once_with(
            bucket_name=os.getenv("DATA_FOLDER_PATH"), folder_path="crop"
        )
        mock_data_loader.load_model_metadata.assert_called_once_with(
            explainer_identifier
        )
        mock_mpm_service.get_metrics.assert_called_once_with(
            model=mock_model,
            data={"mock_key": "mock_value"},
            prediction_target_index=1,
        )

        self.assertEqual(result["precision"], 0.85)
