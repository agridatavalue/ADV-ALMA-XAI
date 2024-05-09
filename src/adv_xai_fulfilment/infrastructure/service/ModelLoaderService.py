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
            {
                "endpoint": os.getenv("MINIO_ENDPOINT"),
                "access_key": os.getenv("MINIO_ACCESS_KEY"),
                "secret_key": os.getenv("MINIO_SECRET_KEY"),
            }
        )
        self._persistenceRepository = PersistenceRepository()

    def load_from(self, model_path: str) -> Model:
        if not Helper.is_local_path(model_path):
            model_path = self._bucketRepository.download_from(model_path)

        with open(model_path, "rb") as file:
            # ciò che ritorna è un'istanza di una classe
            model_data = pickle.load(file)
            logging.info("model_data", model_data)

        os.remove(file)
        return Model(model_data.name)
