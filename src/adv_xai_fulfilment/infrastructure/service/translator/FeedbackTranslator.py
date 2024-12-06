from src.adv_xai_fulfilment.domain.model.questions.Feedback import Feedback


class FeedbackTranslator:
    def translate(self, data: dict) -> Feedback:
        return Feedback(data.get("pilot"), data.get("questions"))

    def translate_many(self, data: list[dict]) -> list[Feedback]:
        return [self.translate(item) for item in data]
