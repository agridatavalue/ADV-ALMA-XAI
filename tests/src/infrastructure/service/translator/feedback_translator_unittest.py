import unittest

from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.questions import Question, Answer
from src.adv_xai_fulfilment.infrastructure.service.translator import FeedbackTranslator

class TestFeedbackTranslator(unittest.TestCase):
    def test_translate(self):
        feedback_translator = FeedbackTranslator()
        data = {
            "partner": "partner",
            "questions": [
                {
                    "id": "id",
                    "question": "question",
                    "answers": [
                        {"value": "value", "type": "type", "label": "label"}
                    ],
                }
            ],
        }
        feedback = feedback_translator.translate(data)
        self.assertIsInstance(feedback.partner, Partner)
        self.assertTrue(all(isinstance(q, Question) for q in feedback.questions))
        self.assertEqual(feedback.questions[0].id, "id")
        self.assertEqual(feedback.questions[0].text, "question")
        self.assertTrue(all(isinstance(q, Answer) for q in feedback.questions[0].possible_answers))
        self.assertEqual(feedback.questions[0].possible_answers[0].value, "value")
        self.assertEqual(feedback.questions[0].possible_answers[0].type, "type")
        self.assertEqual(feedback.questions[0].possible_answers[0].text, "label")
