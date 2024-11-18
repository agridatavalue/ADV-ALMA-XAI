import unittest

from src.adv_xai_fulfilment.domain.model.Model import Model
from src.adv_xai_fulfilment.domain.model.Explainer import Explainer
from src.adv_xai_fulfilment.domain.service.ExplainerRetriever import ExplainerRetriever
from src.adv_xai_fulfilment.domain.model.explainers.KernelSHAPExplainer import (
    KernelSHAPExplainer,
)


class TestExplainerRetriever(unittest.TestCase):
    def setUp(self):
        self.testObj = ExplainerRetriever()

    def test_get_by_data(self):
        model = Model({}, "TEST_name")
        actual = self.testObj.get_by_data(
            model,
            {
                "datatype": "tabular",
                "modeltype": "classification",
                "modelcategory": "tree",
            },
        )
        self.assertIsInstance(actual, list)
        self.assertTrue(all([isinstance(expl, Explainer) for expl in actual]))

    def test_get_by_name(self):
        actual = self.testObj.get_by_name("KernelSHAP")
        self.assertIsInstance(actual, KernelSHAPExplainer)
