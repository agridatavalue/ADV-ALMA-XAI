from ...domain.model.partner import Partner
from ...domain.model.questions import Answer, Question, Feedback
from ...domain.model.explainer_identifier import ExplainerIdentifier
from .explainer_identifier_translator import ExplainerIdentifierTranslator


class FeedbackRequestTranslator:
    _explainer_identifier_translator: ExplainerIdentifierTranslator

    def __init__(self):
        self._explainer_identifier_translator = ExplainerIdentifierTranslator()

    def __translate_question(self, data: dict) -> Question:
        question = Question(
            id=data.get("id", ""),
            text=data.get("text", ""),
            possible_answers=[Answer(value=data.get("answer", ""), type="", text="")],
        )
        question.user_has_answered = data.get("answer", "")
        return question

    def translate_request(self, request: dict) -> Feedback:
        return Feedback(
            partner=Partner(request.get("partner", "")),
            questions=[self.__translate_question(q) for q in request.get("responses", [])],
            explainer_identifier=self._explainer_identifier_translator.translate(
                request=request
            ),
        )
    
    def translate_get_partner_feedback(self, request: dict) -> ExplainerIdentifier:
        return ExplainerIdentifier(
            model=request.get("model", ""),
            partner=Partner(request.get("partner", "")),
            metadata_identifier=request.get("meta_data", ""),
            prediction_target=request.get("prediction_target", ""),
        )
