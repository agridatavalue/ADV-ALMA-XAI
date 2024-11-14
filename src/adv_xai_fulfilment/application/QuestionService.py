import os
import logging

from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)


class QuestionService:
    _data_loader_service: DataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()

    def generate_from_dict(self, metadata_filename: str) -> list[Question]:
        data = None

        if metadata_filename:
            assert metadata_filename, Errors.METADATA_FILENAME_NOT_STRING
            logging.debug(f"loading metadata from {metadata_filename}")
            data: dict = self._data_loader_service.load_meta_data(
                metadata_filename,
                bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
            )

        return [
            q.verticalize_for(data.get("model_metadata")) for q in Question.get_all()
        ]

    def save_user_feedback(
        self, answers: list[dict], metadata_filename: str
    ) -> list[Question]:
        user_answers: list[Question] = []
        for answer in answers:
            for question in Question.get_all():
                if question.id == answer.get("id"):
                    question.user_has_answered = answer.get("answer")
                    user_answers.append(question)
                    break
        return user_answers
