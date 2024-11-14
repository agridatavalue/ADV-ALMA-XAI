from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.application.QuestionService import QuestionService
from .validator.ExplainerIdentifierValidator import ExplainerIdentifierValidator
from .translator.ExplainerIdentifierTranslator import RequestIdentifierTranslator
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class QuestionAndFeedbackPresentation:
    _question_service: QuestionService
    _translator: RequestIdentifierTranslator

    def __init__(self):
        self._question_service = QuestionService()
        self._validator = ExplainerIdentifierValidator()
        self._translator = RequestIdentifierTranslator()

    def get_questions_from_metadata(self, request: dict = {}) -> list[dict]:
        self._validator.validate_questions_(request)
        expl_id: ExplainerIdentifier = self._translator.translate(request)

        return [q.to_dict() for q in self._question_service.generate_from_dict(expl_id)]

    def get_user_feedback_from(self, request: dict = {}) -> bool:
        self._validator.validate_feedback_(request)
        expl_id: ExplainerIdentifier = self._translator.translate(request)

        feedback: list[Question] = self._question_service.save_user_feedback(
            expl_id, request.get("responses")
        )
        return len(feedback) > 0
