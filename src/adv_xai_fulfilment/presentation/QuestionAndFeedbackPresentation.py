from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.application.QuestionService import QuestionService


class QuestionAndFeedbackPresentation:
    _question_service: QuestionService

    def __init__(self):
        self._question_service = QuestionService()

    def get_questions_from_metadata(self, metadata_filename: str) -> list[dict]:
        data = self._question_service.generate_from_dict(metadata_filename)
        print(">>> data:", data)
        return [
            q.to_dict()
            for q in self._question_service.generate_from_dict(metadata_filename)
        ]

    def get_feedback_from(self, data: list) -> bool:
        return True
