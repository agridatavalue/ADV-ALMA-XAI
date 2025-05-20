from datetime import datetime

from ..partner import Partner
from .question import Question
from ..explainer_identifier import ExplainerIdentifier


class Feedback:
    partner: Partner
    questions: list[Question]
    _creation_date: datetime
    _explainer_identifier: ExplainerIdentifier

    def __init__(
        self,
        partner: Partner,
        questions: list[Question] = Question.get_all(),
        explainer_identifier: ExplainerIdentifier = None,
    ):
        self.partner = partner
        self.questions = questions or []
        self._creation_date = datetime.now()
        self._explainer_identifier = explainer_identifier

    @property
    def explainer_identifier(self) -> ExplainerIdentifier:
        return self._explainer_identifier
    
    @property
    def creation_date(self) -> datetime:
        return self._creation_date
    
    @creation_date.setter
    def creation_date(self, value: datetime):
        self._creation_date = value or self._creation_date

    def set_questions(self, questions: list[Question]) -> "Feedback":
        assert isinstance(questions, list), "questions must be a list"
        assert all(
            isinstance(q, Question) for q in questions
        ), "questions must be a list of Question"

        self.questions = questions
        return self

    def to_dict(self) -> dict:
        return {
            "partner": self.partner.id,
            "feedback": [q.to_dict() for q in self.questions],
            "creation_date": self.creation_date.timestamp(),
        }

    def __repr__(self) -> str:
        return f"Feedback(partner={self.partner.id}, creation_date={self.creation_date}, questions={self.questions})"

    @staticmethod
    def create_from(param: any) -> "Feedback":
        if isinstance(param, ExplainerIdentifier):
            return Feedback(Partner(id=param.partner), [])
