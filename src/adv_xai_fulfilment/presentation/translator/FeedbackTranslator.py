from ...domain.model.Pilot import Pilot
from ...domain.model.questions.Feedback import Feedback
from .ExplainerIdentifierTranslator import ExplainerIdentifierTranslator


class FeedbackTranslator:
    _explainer_identifier_translator: ExplainerIdentifierTranslator

    def __init__(self):
        self._explainer_identifier_translator = ExplainerIdentifierTranslator()

    def translate_request(self, request: dict) -> Feedback:
        return Feedback(
            pilot=Pilot(request.get("pilot")),
            questions=[],
            explainer_identifier=self._explainer_identifier_translator.translate(
                request=request
            ),
        )
