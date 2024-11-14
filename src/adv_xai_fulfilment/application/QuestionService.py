import logging

from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)


class QuestionService:
    _data_loader_service: DataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()

    def generate_from_dict(self, expl_id: ExplainerIdentifier) -> list[Question]:
        expl_id.category = "regression"

        logging.debug(f"loading metadata from {expl_id.metadata}")
        data: dict = self._data_loader_service.load_explainer_metadata(expl_id)

        return [
            q.verticalize_for(data.get("model_metadata", {}))
            for q in Question.get_all()
        ]

    def save_user_feedback(
        self, expl_id: ExplainerIdentifier, answers: list[dict]
    ) -> list[Question]:
        user_answers: list[Question] = []
        for answer in answers:
            for question in Question.get_all():
                if question.id == answer.get("id"):
                    question.user_has_answered = answer.get("answer")
                    user_answers.append(question)
                    break
        return user_answers
