import os
import pickle
import logging

from ..Helper import Helper
from ...domain.model.Model import Model
from ...domain.model.explainers.Explainer import Explainer
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
            model_path = self._bucketRepository.download_from(
                bucket_name=os.getenv("MODEL_FOLDER_PATH"), object_name=model_path
            )

        with open(model_path, "rb") as file:
            # ciò che ritorna è un'istanza di una classe
            model_data = pickle.load(file)
            logging.info("model_data", model_data)

        os.remove(file)
        return Model(model_data.name, model_data)

    def upload_to(self, model_path: str, explainer: Explainer):
        with open(
            os.path.join(
                model_path,
                explainer.name + ".pkl",
            ),
            "wb",
        ) as file:
            pickle.dump(explainer.build_result, file)

        self._bucketRepository.upload_to(model_path)
        os.remove(file)
        return model
