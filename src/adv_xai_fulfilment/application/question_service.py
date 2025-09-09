from logger import get_logger

from src.adv_xai_fulfilment.domain.model.questions import Question, Feedback
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService
from ..domain.model.questions.model_feedback_container import ModelFeedbackContainer
from src.adv_xai_fulfilment.domain.model.explainer_metadata import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.infrastructure.repository.feedback_repository import FeedbackRepository
from src.adv_xai_fulfilment.infrastructure.service.explainer_repository_service import (
    ExplainerRepositoryService,
)

logger = get_logger()

class QuestionService:
    _feedback_repository: FeedbackRepository
    _metadata_loader_service: MetaDataLoaderService
    _explainer_repository_service: ExplainerRepositoryService

    def __init__(self):
        self._feedback_repository = FeedbackRepository()
        self._metadata_loader_service = MetaDataLoaderService()
        self._explainer_repository_service = ExplainerRepositoryService()

    def generate_from_dict(self, expl_id: ExplainerIdentifier) -> list[Question]:
        if not expl_id.category:
            expl_id.category = "regression"

        logger.debug(f"loading metadata from {expl_id.metadata_identifier}")
        meta_data: ExplainerMetaData = (
            self._metadata_loader_service.load_explainer_metadata(expl_id)
        )

        return [q.verticalize_for(meta_data.model_metadata) for q in Question.get_all()]
    
    def get_partner_feedback(self, expl_id: ExplainerIdentifier) -> Feedback:
        logger.debug(f"loading metadata from {expl_id.metadata_identifier}")
        meta_data: ExplainerMetaData = (
            self._metadata_loader_service.load_explainer_metadata(expl_id)
        )
        
        parter_feedback:list[Feedback] = meta_data.get_all_feedback(filter_by=expl_id.partner)
        return max(parter_feedback, key=lambda feedback: feedback.creation_date, default=None)


    def save_partner_feedback(self, feedback: Feedback, answers: list[dict]) -> Feedback:
        logger.debug(f"saving feedback {feedback}")

        if not feedback.explainer_identifier.category:
            feedback.explainer_identifier.category = "regression"

        feedback_container: ModelFeedbackContainer = self._feedback_repository.load(
            feedback.explainer_identifier
        )
        feedback_container.add_feedback(feedback)
        self._feedback_repository.store(feedback_container)
        return feedback
