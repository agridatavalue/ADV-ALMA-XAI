import unittest
from unittest.mock import MagicMock, patch

from src.adv_xai_fulfilment.domain.model.model import Model
from src.adv_xai_fulfilment.domain.model.pilot import Pilot
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.application.ModelPerformanceMetricService import (
    ModelPerformanceMetricService,
)
from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    ModelPerformance,
)


class TestModelPerformanceMetricService(unittest.TestCase):
    @patch("os.getenv", return_value="/mock/temp")
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.ModelPerformanceServiceComponent"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.ModelLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.DataLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.MetaDataLoaderService"
    )
    def test_get_data(
        self,
        MockDataLoader,
        MockMPMService,
        MockModelLoader,
        ModelMetaDataService,
        mock_getenv,
    ):
        mock_data_loader = MockDataLoader.return_value
        mock_mpm_service = MockMPMService.return_value
        mock_model_loader = MockModelLoader.return_value
        mock_metadata_loader_service = ModelMetaDataService.return_value

        mock_model = MagicMock(spec=Model)
        mock_model_metadata = MagicMock(spec=ModelMetaData)
        explainer_identifier = ExplainerIdentifier(
            data="data",
            model="mock_model",
            pilot=Pilot("pilot"),
            prediction_target="target",
            metadata_identifier="test_metadata_identifier",
        )

        mock_model_loader.load_from.return_value = mock_model
        mock_data_loader.load_model_metadata.return_value = mock_model_metadata
        mock_model_metadata.first_target_name = "default_target"
        mock_model_metadata.index_of_target_name.return_value = 0
        mock_mpm_service.get_data.return_value = ModelPerformance(
            target="target", y_true=[], y_pred=[]
        )
        mock_metadata_loader_service.load_model_metadata.return_value = (
            mock_model_metadata
        )

        service = ModelPerformanceMetricService()
        service._metadata_loader_service = mock_metadata_loader_service
        service._model_loader_service = mock_model_loader
        service._data_loader_service = mock_data_loader
        service._mdm_service = mock_mpm_service

        result = service.get_data(explainer_identifier)

        self.assertIsInstance(result, ModelPerformance)
        self.assertEqual(result.target, "target")

    @patch("os.getenv", return_value="/mock/temp")
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.DataLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.ModelLoaderService"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.ModelPerformanceServiceComponent"
    )
    @patch(
        "src.adv_xai_fulfilment.application.ModelPerformanceMetricService.MetaDataLoaderService"
    )
    def test_get_metrics(
        self,
        MockDataLoader,
        MockMPMService,
        MockModelLoader,
        ModelMetaDataService,
        mock_getenv,
    ):
        mock_data_loader = MockDataLoader.return_value
        mock_mpm_service = MockMPMService.return_value
        mock_model_loader = MockModelLoader.return_value
        mock_metadata_loader_service = ModelMetaDataService.return_value

        mock_model = MagicMock(spec=Model)
        mock_model_metadata = MagicMock(spec=ModelMetaData)
        explainer_identifier = ExplainerIdentifier(
            data="crop",
            model="mock_model",
            pilot=Pilot("pilot"),
            prediction_target="prediction_target",
            metadata_identifier="test_metadata_identifier",
        )

        mock_model_loader.load_from.return_value = mock_model
        mock_model_metadata.first_target_name = "default_target"
        mock_model_metadata.index_of_target_name.return_value = 1
        mock_data_loader.load_model_metadata.return_value = mock_model_metadata
        mock_mpm_service.get_metrics.return_value = {"precision": 0.85}
        mock_metadata_loader_service.load_model_metadata.return_value = (
            mock_model_metadata
        )

        service = ModelPerformanceMetricService()
        service._metadata_loader_service = mock_metadata_loader_service
        service._model_loader_service = mock_model_loader
        service._data_loader_service = mock_data_loader
        service._mdm_service = mock_mpm_service

        result = service.get_metrics(explainer_identifier)

        self.assertEqual(result["precision"], 0.85)
