import unittest

from src.adv_xai_fulfilment.domain.model import Model, ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers import Explainer
from src.adv_xai_fulfilment.domain.model.explainers import KernelSHAPExplainer
from src.adv_xai_fulfilment.domain.service.ExplainerRetriever import ExplainerRetriever


class TestExplainerRetriever(unittest.TestCase):
    def setUp(self):
        self.testObj = ExplainerRetriever()

    def test_get_by_data(self):
        model = Model({}, "TEST_name")
        actual = self.testObj.get_by_data(
            model,
            ModelMetaData(
                data_type="tabular",
                framework="sklearn",
                algorithm="random_forest",
                model_type="classification",
                target_names=[],
                subject_name="subject_name",
                model_category="CLASSIFICATION",
                feature_descriptions=[],
            ),
        )
        self.assertIsInstance(actual, list)
        self.assertTrue(all([isinstance(expl, Explainer) for expl in actual]))

    def test_get_by_name(self):
        actual = self.testObj.get_by_name("KernelSHAP")
        self.assertIsInstance(actual, KernelSHAPExplainer)
