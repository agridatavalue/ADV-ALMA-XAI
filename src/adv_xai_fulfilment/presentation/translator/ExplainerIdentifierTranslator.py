from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class RequestIdentifierTranslator:
    def translate(self, request: dict) -> ExplainerIdentifier:
        return ExplainerIdentifier(
            data=request.get("data"),
            model=request.get("model"),
            metadata=request.get("metadata"),
            prediction_target=request.get("prediction_target"),
        )
