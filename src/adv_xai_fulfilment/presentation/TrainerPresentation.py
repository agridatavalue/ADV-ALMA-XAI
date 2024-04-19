from src.adv_xai_fulfilment.application.TrainerService import TrainerService


class TrainerPresentation:
    _service: TrainerService

    def __init__(self) -> None:
        self._service = TrainerService()

    def train(self, modelName: str, pilot: str, data: str, metadata: str):
        if not modelName and pilot and metadata:
            raise Exception("Missing required params")

        return self._service.train(modelName, pilot, data, metadata)
