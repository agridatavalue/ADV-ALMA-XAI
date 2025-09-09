from logger import get_logger
from .validator import ExplainerIdentifierValidator
from src.adv_xai_fulfilment.domain.model.questions import Feedback
from src.adv_xai_fulfilment.application.question_service import QuestionService
from .translator import FeedbackRequestTranslator, ExplainerIdentifierTranslator
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier

logger = get_logger()

class QuestionAndFeedbackPresentation:
    _feedback_translator: FeedbackRequestTranslator
    _question_service: QuestionService
    _translator: ExplainerIdentifierTranslator
    _validator: ExplainerIdentifierValidator

    def __init__(self):
        self._question_service = QuestionService()
        self._feedback_translator = FeedbackRequestTranslator()
        self._validator = ExplainerIdentifierValidator()
        self._translator = ExplainerIdentifierTranslator()

    def get_questions_from_metadata(self, request: dict = {}) -> list[dict]:
        logger.info(
            f"called get_questions_from_metadata method with params: {request}"
        )
        data_sanitized = self._validator.validate_and_sanitize_questions_(request)
        expl_id: ExplainerIdentifier = self._translator.translate(data_sanitized)

        return [q.to_dict() for q in self._question_service.generate_from_dict(expl_id)]

    def get_partner_feedback_from(self, request: dict = {}) -> Feedback:
        logger.info(f"called get_partner_feedback_from method with params: {request}")
        sanitized_data: dict = self._validator.validate_and_sanitize_feedback_(request)

        feedback: Feedback = self._feedback_translator.translate_request(sanitized_data)

        return self._question_service.save_partner_feedback(
            feedback, answers=request.get("responses", [])
        )
    
    def get_provided_partner_feedback(self, request: dict = {}) -> Feedback:
        logger.info(f"called get_provided_partner_feedback method with params: {request}")
        sanitized_data: dict = self._validator.validate_and_sanitize_partner_feedback(request)
        expl_id: ExplainerIdentifier = self._feedback_translator.translate_get_partner_feedback(sanitized_data)

        return self._question_service.get_partner_feedback(expl_id)