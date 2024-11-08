from __future__ import annotations
from .Answer import Answer


class Question:
    _id: str
    _text: str
    _template_text: str
    _answers: list[Answer]

    def __init__(
        self, id: str, text: str, answers: list[Answer], template_text: str = ""
    ):
        self._id = id
        self._text = text
        self._answers = answers
        self._template_text = template_text

    @property
    def text(self) -> str:
        return self._text

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "question": self._text,
            "answers": [a.to_dict() for a in self._answers],
        }

    def verticalize_for(self, data: dict) -> Question:
        if not isinstance(data, dict) or not self._template_text:
            return self

        self._text = self._template_text.format(
            **{
                **data,
                "targetnames": (
                    data.get("targetnames")[0]
                    if len(data.get("targetnames")) > 0
                    else ""
                ),
                "action": (
                    "predicts"
                    if data.get("modelcategory") == "Regression"
                    else "classifies"
                ),
            }
        )
        return self

    @staticmethod
    def get_all():
        return [
            Question(
                id="1",
                text="From the explanation, I know how the software tool/algorithm works.",
                template_text="From the explanation, I know how the software algorithm {action} {subjectname} {targetnames}.",
                answers=__radio_answers__,
            ),
            Question(
                id="2",
                text="This explanation of how the software tool/algorithm works is satisfying.",
                template_text="This explanation of how the software {action} {subjectname} {targetnames} is satisfying.",
                answers=__radio_answers__,
            ),
            Question(
                id="3",
                text="This explanation of how the software tool/algorithm works has sufficient detail.",
                template_text="This explanation of how the algorithm {action} {subjectname} {targetnames} has sufficient detail.",
                answers=__radio_answers__,
            ),
            Question(
                id="4",
                text="This explanation of how the software tool/algorithm works seems complete.",
                template_text="This explanation of how the algorithm {action} {subjectname} {targetnames} seems complete.",
                answers=__radio_answers__,
            ),
            Question(
                id="5",
                text="This explanation of how the software tool/algorithm works tells me how to use it.",
                template_text="This explanation of how the algorithm {action} {subjectname} {targetnames} helps me to trust the process.",
                answers=__radio_answers__,
            ),
            Question(
                id="6",
                text="This explanation of how the software tool/algorithm works is useful to my goals.",
                answers=__radio_answers__,
            ),
            Question(
                id="7",
                text="This explanation of the software tool/algorithm shows me how accurate and trustable the tool is.",
                answers=__radio_answers__,
            ),
        ]


__radio_answers__ = [
    Answer.create_radio_answer("Agree", "2"),
    Answer.create_radio_answer("Neutral", "1"),
    Answer.create_radio_answer("Disagree", "0"),
]
