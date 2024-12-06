import logging

from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from src.adv_xai_fulfilment.domain.model.questions.Feedback import Feedback
from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)
from src.adv_xai_fulfilment.infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)


class QuestionService:
    _data_loader_service: DataLoaderService
    _explainer_repository_service: ExplainerRepositoryService

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._explainer_repository_service = ExplainerRepositoryService()

    def generate_from_dict(self, expl_id: ExplainerIdentifier) -> list[Question]:
        if not expl_id.category:
            expl_id.category = "regression"

        logging.debug(f"loading metadata from {expl_id.metadata}")
        meta_data: ExplainerMetaData = (
            self._data_loader_service.load_explainer_metadata(expl_id)
        )

        return [q.verticalize_for(meta_data.model_metadata) for q in Question.get_all()]

    def save_pilot_feedback(self, feedback: Feedback, answers: list[dict]) -> Feedback:
        for q in feedback.questions:
            for a in answers:
                if q.id == a.get("id"):
                    q.user_has_answered = a.get("answer")
                    break

        logging.debug(f"loading metadata from {feedback.explainer_identifier.metadata}")
        meta_data: ExplainerMetaData = (
            self._data_loader_service.load_explainer_metadata(
                feedback.explainer_identifier
            )
        )

        meta_data.add_feedback(feedback)
        self._explainer_repository_service.upload_metadata(
            feedback.explainer_identifier, meta_data
        )
        return feedback
