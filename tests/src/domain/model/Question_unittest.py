import unittest

from src.adv_xai_fulfilment.domain.model.questions.Answer import Answer
from src.adv_xai_fulfilment.domain.model.questions.Question import Question


class TestQuestion(unittest.TestCase):

    def test_get_all(self):
        testObj = Question.get_all()
        self.assertIsInstance(testObj, list)
        self.assertEqual(len(testObj), 7)
        self.assertIsInstance(testObj[0], Question)

    def test_verticalize_for(self):
        testObj = Question(
            id="1",
            text="From the explanation, I know how the software tool/algorithm works.",
            template_text="From the explanation, I know how the software algorithm {action} {subjectname} {targetname}.",
            answers=[],
        )
        self.assertEqual(
            testObj.verticalize_for(
                {
                    "subjectname": "leek",
                    "targetname": "targetname",
                    "modelcategory": "Regression",
                }
            ).text,
            "From the explanation, I know how the software algorithm predicts leek targetname.",
        )

        testObj = Question(
            id="1",
            text="From the explanation, I know how the software tool/algorithm works.",
            answers=[],
        )
        self.assertEqual(
            testObj.verticalize_for(None).text,
            "From the explanation, I know how the software tool/algorithm works.",
        )

    def test_to_dict(self):
        testObj = Question(
            id="1",
            text="From the explanation, I know how the software tool/algorithm works.",
            answers=[],
        )

        self.assertEqual(
            testObj.to_dict(),
            {
                "id": "1",
                "question": "From the explanation, I know how the software tool/algorithm works.",
                "answers": [],
            },
        )

    def test_user_has_answered(self):
        testObj = Question(
            id="1",
            text="From the explanation, I know how the software tool/algorithm works.",
            answers=[Answer("radio", "text", "value")],
        )

        testObj.user_has_answered = "value"
        self.assertEqual(testObj.user_has_answered, "value")
        self.assertIsInstance(testObj._user_answer, Answer)
