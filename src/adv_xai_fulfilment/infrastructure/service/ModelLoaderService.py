import os
import logging

from ..repository.BucketRepository import BucketRepository
from src.adv_xai_fulfilment.domain.model.Model import Model
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.service.ModelTranslator import ModelTranslator


class ModelLoaderService:
    _model_translator: ModelTranslator
    _bucketRepository: BucketRepository

    def __init__(self):
        self._bucketRepository = BucketRepository(
            {
                "endpoint": os.getenv("MINIO_ENDPOINT"),
                "access_key": os.getenv("MINIO_ACCESS_KEY"),
                "secret_key": os.getenv("MINIO_SECRET_KEY"),
                "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
            }
        )
        self._model_translator = ModelTranslator()

    def load_from(self, model_file_path: str, meta_data: ModelMetaData) -> Model:
        model_local_file_path: str = Model.get_locale_filepath(model_file_path)
        logging.debug(f"loading model from {model_file_path} to {model_file_path}")

        if not os.path.exists(model_local_file_path):
            model_file_path: str = self._bucketRepository.download_from(
                object_name=model_file_path,
                bucket_name=os.getenv("MODEL_FOLDER_PATH"),
                destination_file_path=model_local_file_path,
            )

        logging.debug(
            f"select domain model for: framework {meta_data.framework} and algoritm {meta_data.algorithm}"
        )
        return (
            self._model_translator.with_(meta_data.framework)
            .and_(meta_data.algorithm)
            .translate(model_local_file_path)
        )
