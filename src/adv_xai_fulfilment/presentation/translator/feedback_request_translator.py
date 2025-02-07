from ...domain.model.pilot import Pilot
from ...domain.model.questions import Answer, Question, Feedback
from .explainer_identifier_translator import ExplainerIdentifierTranslator


class FeedbackRequestTranslator:
    _explainer_identifier_translator: ExplainerIdentifierTranslator

    def __init__(self):
        self._explainer_identifier_translator = ExplainerIdentifierTranslator()

    def __translate_question(self, data: dict) -> Question:
        question = Question(
            id=data.get("id"),
            text=data.get("text"),
            answers=[Answer(value=data.get("answer"), type=None, text=None)],
        )
        question.user_has_answered = data.get("answer")
        return question

    def translate_request(self, request: dict) -> Feedback:
        return Feedback(
            pilot=Pilot(request.get("pilot")),
            questions=[self.__translate_question(q) for q in request.get("responses")],
            explainer_identifier=self._explainer_identifier_translator.translate(
                request=request
            ),
        )
