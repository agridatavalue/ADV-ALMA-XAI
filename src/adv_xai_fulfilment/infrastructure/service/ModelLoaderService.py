from src.adv_xai_fulfilment.domain.model.Model import Model
from ..repository.PersistenceRepository import PersistenceRepository


class ModelLoaderService:
    _persistenceRepository: PersistenceRepository

    def __init__(self):
        self._persistenceRepository = PersistenceRepository()

    def loadFrom(self, file_path: str) -> list[Model]:
        return [
            Model(
                name=data.get("name"),
                type=data.get("modeltype"),
                category=data.get("modelcategory"),
                data_type=data.get("datatype"),
                explanations=data.get("explanations"),
                is_distributed=data.get("distributed"),
                train_set_required=data.get("train_set_required"),
                has_categorical_features=data.get("categorical_features"),
            )
            for data in self._persistenceRepository.read(file_path).get("models")
        ]
