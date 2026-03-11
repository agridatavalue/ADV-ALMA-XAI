import json
from os import path

from .answer import Answer


class Question:
    _id: str
    _text: str
    _template_text: str
    _possible_answers: list[Answer]
    _user_answer: Answer

    def __init__(
        self, id: str, text: str, possible_answers: list[Answer], template_text: str = ""
    ):
        self._id = id
        self._text = text
        self._user_answer = None
        self._template_text = template_text
        self._possible_answers = possible_answers

    @property
    def id(self) -> str:
        return self._id

    @property
    def text(self) -> str:
        return self._text
    
    @property
    def possible_answers(self) -> list[Answer]:
        return self._possible_answers

    @property
    def user_has_answered(self) -> str:
        return self._user_answer.value if self._user_answer else ""

    @user_has_answered.setter
    def user_has_answered(self, value: str):
        self._user_answer = next((a for a in self._possible_answers if a.value == value), None)

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "question": self._text,
            "feedback": self._user_answer.value if self._user_answer else "",
            "answers": {
                "type": "value",
                "values": [ 
                    { "label": a.text, "value": a.value } for a in self._possible_answers]
            },
        }

    def verticalize_for(self, data: dict) -> "Question":
        if not isinstance(data, dict) or not self._template_text:
            return self

        self._text = self._template_text.format(
            **{
                **data,
                "targetname": data.get("targetname"),
                "action": (
                    "predicts"
                    if data.get("modelcategory", "").lower() == "regression"
                    else "classifies"
                ),
            }
        )
        return self

    def __repr__(self) -> str:
        return 'Question(id="{}", text="{}" {})'.format(
            self._id,
            self._text,
            f"feedback={self._user_answer.value}" if self._user_answer else "",
        )

    @staticmethod
    def get_all() -> list["Question"]:
        file_path: str = path.abspath(
            path.join(
                path.dirname(__file__),
                "../../../../../",
                "sources",
                "values_questions.json",
            )
        )
        with open(file_path) as file:
            data: dict = json.load(file) or {}
            return [
                Question(
                    **d,
                    possible_answers=[
                        Answer.create_value_answer("00% Disagree", "0"),
                        Answer.create_value_answer("10% Slightly Agree", "1"),
                        Answer.create_value_answer("20% Somewhat Agree", "2"),
                        Answer.create_value_answer("30% Moderately Agree", "3"),
                        Answer.create_value_answer("40% Fairly Agree", "4"),
                        Answer.create_value_answer("50% Mostly Agree", "5"),
                        Answer.create_value_answer("60% Strongly Agree", "6"),
                        Answer.create_value_answer("70% Very Strongly Agree", "7"),
                        Answer.create_value_answer("80% Highly Agree", "8"),
                        Answer.create_value_answer("90+% Totally Agree", "9"),
                    ],
                )
                for d in data.get("data", [])
            ]
