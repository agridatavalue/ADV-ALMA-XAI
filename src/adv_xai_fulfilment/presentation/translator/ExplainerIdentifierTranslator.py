from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class ExplainerIdentifierTranslator:
    def translate(self, request: dict) -> list[ExplainerIdentifier]:
        return [
            ExplainerIdentifier(
                data=request.get("data"),
                model=request.get("model"),
                metadata=request.get("metadata", request.get("meta_data")),
                pilot=Pilot(request.get("pilot")),
                prediction_target=pred,
            )
            for pred in request.get(
                "prediction_targets", [request.get("prediction_target")]
            )
        ]
