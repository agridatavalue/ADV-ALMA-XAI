import unittest
from unittest.mock import Mock


from src.adv_xai_fulfilment.domain.model.data_type import DataType
from src.adv_xai_fulfilment.domain.model.model_context import ModelContext
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.explainer import Explainer
from src.adv_xai_fulfilment.domain.model.explainers.datatype_model_explainer import (
    DataTypeModelExplainer,
)


class TestExplainer(unittest.TestCase):
    def setUp(self):
        self.testObj = Explainer(
            name="name",
            type=["BlackBox"],
            categories=["Regression"],
            explanations="explanations",
            is_distributed=True,
            train_set_required=True,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TEXT, "explanations")
            ],
        )

    def test_set_meta_data(self):
        self.assertIsNone(self.testObj.meta_data)
        meta_data = ModelMetaData(
            data_type="Text",
            algorithm="algorithm",
            framework="framework",
            model_type="BlackBox",
            subject_name="subject_name",
            target_names=[],
            project_theme="project_theme",
            model_category="Regression",
            feature_descriptions=[],
        )
        self.testObj.set_meta_data(meta_data)
        self.assertEqual(self.testObj.meta_data, meta_data)

    def test_can_match_with(self):
        self.assertTrue(
            self.testObj.can_match_with(
                context=ModelContext(
                    model=None,
                    model_metadata=ModelMetaData(
                        data_type="Text",
                        algorithm="algorithm",
                        framework="framework",
                        model_type="BlackBox",
                        subject_name="subject_name",
                        target_names=[],
                        project_theme="project_theme",
                        model_category="Regression",
                        feature_descriptions=[],
                    ),
                    model_data=None,
                    identifier=None,
                )
            )
        )

        some_model = Mock()
        some_model_data = Mock()
        some_identifier = Mock()

        # Mock ModelMetaData with required attributes
        mock_model_metadata = Mock()
        mock_model_metadata.model_type = "type"
        mock_model_metadata.model_category = "category"
        mock_model_metadata.data_type = "tabular"

        # Your test
        self.assertFalse(
            self.testObj.can_match_with(
                ModelContext(
                    model=some_model,
                    model_data=some_model_data,
                    model_metadata=mock_model_metadata,
                    identifier=some_identifier
                )
            )
        )
