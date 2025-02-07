import logging

from src.adv_xai_fulfilment.domain.model.questions import Feedback, Question
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService
from src.adv_xai_fulfilment.domain.model.explainer_metadata import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)


class QuestionService:
    _metadata_loader_service: MetaDataLoaderService
    _explainer_repository_service: ExplainerRepositoryService

    def __init__(self):
        self._metadata_loader_service = MetaDataLoaderService()
        self._explainer_repository_service = ExplainerRepositoryService()

    def generate_from_dict(self, expl_id: ExplainerIdentifier) -> list[Question]:
        if not expl_id.category:
            expl_id.category = "regression"

        logging.debug(f"loading metadata from {expl_id.metadata_identifier}")
        meta_data: ExplainerMetaData = (
            self._metadata_loader_service.load_explainer_metadata(expl_id)
        )

        return [q.verticalize_for(meta_data.model_metadata) for q in Question.get_all()]

    def save_pilot_feedback(self, feedback: Feedback, answers: list[dict]) -> Feedback:
        if not feedback.explainer_identifier.category:
            feedback.explainer_identifier.category = "regression"

        logging.debug(f"loading metadata from {feedback.explainer_identifier.metadata}")
        meta_data: ExplainerMetaData = (
            self._metadata_loader_service.load_explainer_metadata(
                feedback.explainer_identifier
            )
        )
        meta_data.add_feedback(feedback)
        self._explainer_repository_service.upload_metadata(
            feedback.explainer_identifier, meta_data
        )
        return feedback
