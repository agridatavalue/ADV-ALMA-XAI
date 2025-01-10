from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class ExplainerIdentifierTranslator:
    def translate(self, request: dict) -> ExplainerIdentifier:
        return ExplainerIdentifier(
            data=request.get("data"),
            model=request.get("model"),
            pilot=Pilot(request.get("pilot")),
            metadata=ModelMetaData(
                request.get("meta_data", request.get("metadata", {}))
            ),
            prediction_target=request.get("prediction_target"),
        )
