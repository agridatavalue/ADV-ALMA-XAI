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

    def load_from(self, model_file_path: str) -> Model:
        logging.debug(f"loading model from {model_file_path}")

        if not Helper.is_local_path(model_file_path):
            logging.debug(
                f"is not a local path, downloading {model_file_path} from {os.getenv('MODEL_FOLDER_PATH')}"
            )
            model_file_path: str = self._bucketRepository.download_from(
                bucket_name=os.getenv("MODEL_FOLDER_PATH"), object_name=model_file_path
            )

        with open(model_file_path, "rb") as file:
            # ciò che ritorna è un'istanza di una classe
            model_data = pickle.load(file)

        os.remove(model_file_path)
        return Model(handler=model_data)

    def upload_to(self, model_path: str, explainer: Explainer):
        assert isinstance(explainer, Explainer)

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
