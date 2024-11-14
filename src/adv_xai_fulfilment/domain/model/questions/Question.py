from __future__ import annotations
import json
from os import path

from .Answer import Answer


class Question:
    _id: str
    _text: str
    _template_text: str
    _answers: list[Answer]
    _user_answer: Answer

    def __init__(
        self, id: str, text: str, answers: list[Answer], template_text: str = ""
    ):
        self._id = id
        self._text = text
        self._answers = answers
        self._user_answer = None
        self._template_text = template_text

    @property
    def id(self) -> str:
        return self._id

    @property
    def text(self) -> str:
        return self._text

    @property
    def user_has_answered(self) -> str:
        return self._user_answer.value if self._user_answer else ""

    @user_has_answered.setter
    def user_has_answered(self, value: str) -> bool:
        self._user_answer = next((a for a in self._answers if a.value == value), None)

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
    def get_all() -> list[Question]:
        file_path = path.abspath(
            path.join(
                path.dirname(__file__),
                "../../../../../",
                "sources",
                "radio_questions.json",
            )
        )
        with open(file_path) as file:
            data: dict = json.load(file) or {}
            return [
                Question(
                    **d,
                    answers=[
                        Answer.create_radio_answer("Agree", "agree"),
                        Answer.create_radio_answer("Neutral", "neutral"),
                        Answer.create_radio_answer("Disagree", "disagree"),
                    ],
                )
                for d in data.get("data", [])
            ]
