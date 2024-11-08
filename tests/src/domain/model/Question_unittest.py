import unittest

from src.adv_xai_fulfilment.domain.model.questions.Question import Question


class TestQuestion(unittest.TestCase):

    def test_verticalize_for(self):
        testObj = Question(
            id="1",
            text="From the explanation, I know how the software tool/algorithm works.",
            template_text="From the explanation, I know how the software algorithm {action} {subjectname} {targetnames}.",
            answers=[],
        )
        self.assertEqual(
            testObj.verticalize_for(
                {
                    "subjectname": "leek",
                    "targetnames": ["targetname"],
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
