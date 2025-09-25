import unittest

from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier

class TestExplainerIdentifier(unittest.TestCase):
    def test_get_explainer_file_path(self):
        explainer_id = ExplainerIdentifier(
            model="models/sample_model",
            partner=Partner(id="partner1"),
            metadata_identifier="meta1",
            prediction_target="target1",
            data="data1"
        )
        explainer_id.category = "classification"  # Normally set via metadata
        expected_path = "explainers/sample_model/target1_classification/partner1/filename.ext"
        actual_path = explainer_id.get_explainer_file_path("filename.ext")
        self.assertEqual(expected_path, actual_path)