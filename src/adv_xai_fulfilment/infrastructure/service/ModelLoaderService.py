import os
import pickle
import logging

from ..Helper import Helper
from ...domain.model.Model import Model
from ..repository.BucketRepository import BucketRepository
from ..repository.PersistenceRepository import PersistenceRepository


class ModelLoaderService:
    _bucketRepository: BucketRepository
    _persistenceRepository: PersistenceRepository

    def __init__(self):
        self._bucketRepository = BucketRepository(
            {"endpoint": "", "access_key": "", "secret_key": "", "bucket": ""}
        )
        self._persistenceRepository = PersistenceRepository()

    def loadFrom(self, model_path: str) -> Model:
        if not Helper.is_local_path(model_path):
            model_path = self._bucketRepository.downloadFrom(model_path)

        with open(model_path, "rb") as file:
            # ciò che ritorna è un'istanza di una classe
            model_data = pickle.load(file)
            logging.info("model_data", model_data)

        os.remove(file)
        return Model(model_data.name)
