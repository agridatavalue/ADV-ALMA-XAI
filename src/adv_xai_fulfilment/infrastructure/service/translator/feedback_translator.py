from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.questions import Answer, Question, Feedback


class FeedbackTranslator:
    def __translate_answers(self, data: list[dict]) -> list[Answer]:
        return [
            Answer(
                value=item.get("value"), type=item.get("type"), text=item.get("label")
            )
            for item in data
        ]

    def __translate_questions(self, data: list[dict]) -> list[Question]:
        return [
            Question(
                id=item.get("id"),
                text=item.get("text"),
                answers=self.__translate_answers(item.get("answers", [])),
            )
            for item in data
        ]

    def translate(self, data: dict) -> Feedback:
        return Feedback(
            partner=Partner(data.get("partner")),
            questions=self.__translate_questions(data.get("questions")),
        )

    def translate_many(self, data: list[dict]) -> list[Feedback]:
        return [self.translate(item) for item in data]
