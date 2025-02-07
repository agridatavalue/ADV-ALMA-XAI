import logging

from src.adv_xai_fulfilment.domain.model.questions import Feedback
from src.adv_xai_fulfilment.domain.model import ExplainerIdentifier
from src.adv_xai_fulfilment.application.QuestionService import QuestionService

from .translator.FeedbackRequestTranslator import FeedbackRequestTranslator
from .validator.ExplainerIdentifierValidator import ExplainerIdentifierValidator
from .translator.ExplainerIdentifierTranslator import ExplainerIdentifierTranslator


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
        logging.info(
            f"called get_questions_from_metadata method with params: {request}"
        )
        self._validator.validate_and_sanitize_questions_(request)
        expl_id: ExplainerIdentifier = self._translator.translate(request)

        return [q.to_dict() for q in self._question_service.generate_from_dict(expl_id)]

    def get_pilot_feedback_from(self, request: dict = {}) -> bool:
        logging.info(f"called get_user_feedback_from method with params: {request}")
        self._validator.validate_and_sanitize_feedback_(request)

        feedback: Feedback = self._feedback_translator.translate_request(request)

        return self._question_service.save_pilot_feedback(
            feedback, answers=request.get("responses", [])
        )
