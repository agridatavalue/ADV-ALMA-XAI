import unittest

from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.questions.feedback import Feedback
from src.adv_xai_fulfilment.domain.model.questions.model_feedback_container import (
    ModelFeedbackContainer,
)
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier

class TestModelFeedbackContainer(unittest.TestCase):
    def test_get_feedback_for_partner(self):
        container = ModelFeedbackContainer(filepath="test_path")
        
        partner1 = Partner(id="partner_1")
        partner2 = Partner(id="partner_2")
        
        explainer_id1 = ExplainerIdentifier(
            model="model_1",
            partner=partner1,
            metadata_identifier="meta_1",
            prediction_target="target_1",
        )
        explainer_id2 = ExplainerIdentifier(
            model="model_2",
            partner=partner2,
            metadata_identifier="meta_2",
            prediction_target="target_2",
        )
        
        feedback1 = Feedback(partner=partner1, questions=[], explainer_identifier=explainer_id1)
        feedback2 = Feedback(partner=partner2, questions=[], explainer_identifier=explainer_id2)
        feedback3 = Feedback(partner=partner1, questions=[], explainer_identifier=explainer_id1)
        
        container.add_feedback(feedback1)
        container.add_feedback(feedback2)
        container.add_feedback(feedback3)
        
        result_partner1 = container.get_feedback_for_partner(partner1)
        result_partner2 = container.get_feedback_for_partner(partner2)
        
        self.assertEqual(len(result_partner1), 2)
        self.assertIn(feedback1, result_partner1)
        self.assertIn(feedback3, result_partner1)
        
        self.assertEqual(len(result_partner2), 1)
        self.assertIn(feedback2, result_partner2)
        
    def test_to_dict(self):
        container = ModelFeedbackContainer(filepath="test_path")
        
        partner = Partner(id="partner_1")
        explainer_id = ExplainerIdentifier(
            model="model_1",
            partner=partner,
            metadata_identifier="meta_1",
            prediction_target="target_1",
        )
        
        feedback = Feedback(partner=partner, questions=[], explainer_identifier=explainer_id)
        container.add_feedback(feedback)
        
        result_dict = container.to_dict()
        
        self.assertIn("improvements", result_dict)
        self.assertIn("feedback", result_dict)
        self.assertEqual(len(result_dict["feedback"]), 1)
        self.assertEqual(result_dict["feedback"][0], feedback.to_dict())