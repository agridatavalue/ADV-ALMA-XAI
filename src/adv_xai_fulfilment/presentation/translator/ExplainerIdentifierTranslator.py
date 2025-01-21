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
            for pred in request.get(
                "prediction_targets", [request.get("prediction_target", [])]
            )
        ]

    def translate(self, request: dict) -> ExplainerIdentifier:
        return self.translate_many(request)[0]
