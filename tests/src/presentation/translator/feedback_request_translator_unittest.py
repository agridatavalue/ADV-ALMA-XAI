import unittest

from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.questions import Question, Feedback
from src.adv_xai_fulfilment.presentation.translator import FeedbackRequestTranslator


class TestFeedbackRequestTranslator(unittest.TestCase):
    def test_translate_request(self):
        translator = FeedbackRequestTranslator()
        feedback = translator.translate_request(
            {
                "partner": "partner",
                "responses": [{"id": "id", "text": "text", "answer": "answer"}],
            }
        )

        self.assertIsInstance(feedback, Feedback)
        self.assertIsInstance(feedback.partner, Partner)
        self.assertIsInstance(feedback.questions, list)
        self.assertTrue(all([isinstance(q, Question) for q in feedback.questions]))
