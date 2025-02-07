import unittest

from src.adv_xai_fulfilment.domain.model.pilot import Pilot
from src.adv_xai_fulfilment.domain.model.questions import Question, Feedback
from src.adv_xai_fulfilment.presentation.translator import FeedbackRequestTranslator


class TestFeedbackRequestTranslator(unittest.TestCase):
    def test_translate_request(self):
        translator = FeedbackRequestTranslator()
        feedback = translator.translate_request(
            {
                "pilot": "pilot",
                "responses": [{"id": "id", "text": "text", "answer": "answer"}],
            }
        )

        self.assertIsInstance(feedback, Feedback)
        self.assertIsInstance(feedback.pilot, Pilot)
        self.assertIsInstance(feedback.questions, list)
        self.assertTrue(all([isinstance(q, Question) for q in feedback.questions]))
