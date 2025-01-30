from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class ExplainerIdentifierTranslator:
    def translate_many(self, request: dict) -> list[ExplainerIdentifier]:
        return [
            ExplainerIdentifier(
                prediction_target=pred,
                data=request.get("data"),
                model=request.get("model"),
                pilot=Pilot(request.get("pilot")),
                metadata_identifier=request.get("metadata", request.get("meta_data")),
            )
            for pred in self.__get_prediction_targets(request)
        ]

    def translate(self, request: dict) -> ExplainerIdentifier:
        return self.translate_many(request)[0]

    def __get_prediction_targets(self, request: dict) -> list[str]:
        if request.get("prediction_target"):
            return [request.get("prediction_target")]

        if request.get("prediction_targets"):
            return request.get("prediction_targets")

        return [""]
