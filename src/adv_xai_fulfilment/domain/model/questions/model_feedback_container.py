from ..partner import Partner
from .feedback import Feedback

class ModelFeedbackContainer:
    _filepath: str
    _feedback: list[Feedback]
    _improvements: list[dict]

    def __init__(self, filepath: str):
        self._feedback = []
        self._improvements = []
        self._filepath = filepath

    def get_filepath(self) -> str:
        return self._filepath

    def add_feedback(self, feedback: Feedback) -> "ModelFeedbackContainer":
        assert isinstance(feedback, Feedback), "Feedback must be of type Feedback, got {}".format(type(feedback))

        self._feedback.append(feedback)
        return self
    
    def get_feedback_for_partner(self, partner: Partner) -> list[Feedback]:
        return [f for f in self._feedback if f.partner.is_equal(partner)]
    
    def to_dict(self) -> dict:
        return {
            "improvements": [],
            "feedback": [f.to_dict() for f in self._feedback],
        }
