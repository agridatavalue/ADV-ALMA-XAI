import unittest

from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.domain.model.questions.Feedback import Feedback
from src.adv_xai_fulfilment.presentation.translator.FeedbackRequestTranslator import (
    FeedbackRequestTranslator,
)


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
