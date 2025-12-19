import unittest

from src.adv_xai_fulfilment.domain.model.model import Model
from src.adv_xai_fulfilment.domain.service import ExplainerRetriever
from src.adv_xai_fulfilment.domain.model.model_context import ModelContext
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.explainer import Explainer
from src.adv_xai_fulfilment.domain.model.explainers import KernelSHAPExplainer
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier


class TestExplainerRetriever(unittest.TestCase):
    def setUp(self):
        self.testObj = ExplainerRetriever()

    def test_get_by_data(self):
        context = ModelContext(
            model = Model({}, "TEST_name"),
            model_metadata = ModelMetaData(
                data_type="tabular",
                framework="sklearn",
                algorithm="random_forest",
                model_type="classification",
                target_names=[],
                subject_name="subject_name",
                project_theme="project_theme",
                model_category="CLASSIFICATION",
                feature_descriptions=[],
            ),
            identifier = ExplainerIdentifier(
                model="TEST_name",
                partner="TEST_partner",
                metadata_identifier="TEST_metadata_identifier",
                prediction_target="TEST_prediction_target",
                data="TEST_data",
                data_for_training="TEST_data_for_training",
            ),
            model_data=None,
        )
        
        actual = self.testObj.get_by_data(context)
        self.assertIsInstance(actual, list)
        self.assertTrue(all([isinstance(expl, Explainer) for expl in actual]))

    def test_get_by_name(self):
        actual = self.testObj.get_by_name("KernelSHAP")
        self.assertIsInstance(actual, KernelSHAPExplainer)
