import json
from os import path
from logger import get_logger
from datetime import datetime

from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.questions.answer import Answer
from src.adv_xai_fulfilment.domain.model.questions.feedback import Feedback
from src.adv_xai_fulfilment.domain.model.questions.question import Question
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.domain.model.questions.model_feedback_container import ModelFeedbackContainer

logger = get_logger()

class FeedbackFileToFeedbackContainerTranslator:

    def translate(self, explainer_identifier: ExplainerIdentifier) -> ModelFeedbackContainer:
        if not isinstance(explainer_identifier, ExplainerIdentifier):
            raise TypeError("explainer_identifier must be an instance of ExplainerIdentifier")

        container = ModelFeedbackContainer(explainer_identifier.get_feedback_file_locale_path())
        if not path.exists(container.get_filepath()):
            logger.debug(f"Feedback file {container.get_filepath()} does not exist.")
            return container
        
        with open(container.get_filepath(), "r") as file:
            feedback_data: dict = json.load(file)

            for feedback in feedback_data.get("feedback", []):
                translated_feedback = self._translate_feedback(feedback, explainer_identifier)
                container.add_feedback(translated_feedback)

        return container

    def _translate_feedback(self, feedback_data: dict, explainer_identifier: ExplainerIdentifier) -> Feedback:
        if not isinstance(feedback_data, dict):
            raise TypeError("feedback_data must be a dictionary")

        feedback = Feedback(
            partner = Partner(feedback_data.get("partner", "")),
            questions = [
                self._translate_question(q)
                for q in feedback_data.get("feedback", [])
            ],
            explainer_identifier = explainer_identifier,
        )
        feedback.creation_date = datetime.fromtimestamp(feedback_data.get('creation_date', datetime.now()))
        return feedback
    
    def _translate_question(self, question_data: dict) -> Question:
        assert isinstance(question_data, dict), "question_data must be a dictionary"
        
        question_object = Question(
            id=question_data.get('id', ''),
            text=question_data.get('question', ''),
            possible_answers=[Answer(value=question_data.get('feedback', ''), type='', text='')],
        )
        question_object.user_has_answered = question_data.get('feedback', '')
        return question_object