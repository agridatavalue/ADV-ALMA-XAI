import json
from logger import get_logger

from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.domain.model.questions.model_feedback_container import ModelFeedbackContainer
from .translator.feedback_file_to_feedback_container_translator import FeedbackFileToFeedbackContainerTranslator

logger = get_logger()

class FeedbackRepository:
    _feedback_file_translator: FeedbackFileToFeedbackContainerTranslator
    
    def __init__(self):
        self._feedback_file_translator = FeedbackFileToFeedbackContainerTranslator()

    def load(self, explainer_identifier: ExplainerIdentifier) -> ModelFeedbackContainer:
        logger.debug(f"loading feedback file from {explainer_identifier.get_feedback_file_locale_path()}")

        return self._feedback_file_translator.translate(
            explainer_identifier
        )
        

    def store(self, feedback_container: ModelFeedbackContainer) -> bool:
        logger.debug(f"storing feedback file to {feedback_container.get_filepath()}")

        with open(feedback_container.get_filepath(), "w") as file:
            json.dump(feedback_container.to_dict(), file, indent=4)

        return True