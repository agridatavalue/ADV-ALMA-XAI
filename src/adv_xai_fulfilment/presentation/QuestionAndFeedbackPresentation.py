from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.application.QuestionService import QuestionService


class QuestionAndFeedbackPresentation:
    _question_service: QuestionService

    def __init__(self):
        self._question_service = QuestionService()

    def get_questions_from_metadata(self, metadata_filename: str) -> list[dict]:
        return [
            q.to_dict()
            for q in self._question_service.generate_from_dict(metadata_filename)
        ]

    def get_user_feedback_from(self, data: list[dict]) -> bool:
        feedback: list[Question] = self._question_service.save_user_feedback(data)
        return len(feedback) > 0
