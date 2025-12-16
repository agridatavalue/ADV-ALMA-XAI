import unittest
import pandas as pd
from unittest.mock import MagicMock

from src.adv_xai_fulfilment.domain.model.model import Model
from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.model_data import ModelData
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.application.partial_dependence_service import (
    PartialDependenceService,
)
from src.adv_xai_fulfilment.infrastructure.service.data_loader_service import (
    DataLoaderService,
)
from src.adv_xai_fulfilment.infrastructure.service.model_loader_service import (
    ModelLoaderService,
)
from src.adv_xai_fulfilment.infrastructure.service.metadata_loader_service import (
    MetaDataLoaderService,
)
from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    PartialDependence,
)


class MyModel(Model):
    def __init__(self, filename, layers: list = []):
        super().__init__(filename, layers=layers)

    def is_ok(self):
        return True



class TestPartialDependenceService(unittest.TestCase):
    def test_get_data(self):
        mock_data_loader_service = MagicMock(spec=DataLoaderService)
        mock_data_loader_service.load_data.return_value = ModelData()

        mock_model_loader_service = MagicMock(spec=ModelLoaderService)
        mock_model_data = ModelData()
        mock_model_data.x_train = pd.DataFrame({
            "feature": [1, 2, 3, 4, 5]
        })
        mock_model_data.y_train = pd.Series([10, 20, 30, 40, 50])
        mock_data_loader_service.load_data.return_value = mock_model_data

        mock_metadata_loader_service = MagicMock(spec=MetaDataLoaderService)
        mock_metadata_loader_service.load_model_metadata.return_value = ModelMetaData(
            data_type="TABULAR",
            framework="framework",
            algorithm="algorithm",
            model_type="model_type",
            subject_name="subject_name",
            project_theme="project_theme",
            model_category="regression",
            feature_names=["feature"],
            target_names=["target"]
        )

        testObj = PartialDependenceService()
        testObj._data_loader_service = mock_data_loader_service
        testObj._model_loader_service = mock_model_loader_service
        testObj._metadata_loader_service = mock_metadata_loader_service

        result = testObj.get_data(
            request=ExplainerIdentifier(
                model="model",
                partner=Partner("partner"),
                prediction_target="prediction_target",
                metadata_identifier="metadata_identifier",
            ),
            feature="feature",
        )

        self.assertIsInstance(result, PartialDependence)
