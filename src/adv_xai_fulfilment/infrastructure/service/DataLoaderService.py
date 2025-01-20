import os
import logging
import pandas as pd

from ..repository.BucketRepository import BucketRepository
from .translator.ModelMetaDataTranslator import ModelMetaDataTranslator
from .translator.ExplainerMetaDataTranslator import ExplainerMetaDataTranslator
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class DataLoaderService:
    _bucketRepository: BucketRepository
    _model_metadata_translator: ModelMetaDataTranslator
    _explainer_metadata_translator: ExplainerMetaDataTranslator

    def __init__(self):
        self._bucketRepository = BucketRepository(
            {
                "endpoint": os.getenv("MINIO_ENDPOINT"),
                "access_key": os.getenv("MINIO_ACCESS_KEY"),
                "secret_key": os.getenv("MINIO_SECRET_KEY"),
                "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
            }
        )
        self._model_metadata_translator = ModelMetaDataTranslator()
        self._explainer_metadata_translator = ExplainerMetaDataTranslator()

    def load_data(self, expl_id: ExplainerIdentifier) -> dict[str, pd.DataFrame]:
        if not expl_id.data:
            return None

        to_return = {}
        for file in ["x.csv", "y.csv"]:
            current_file = expl_id.get_data_locale_filepath(file)
            if not os.path.exists(current_file):
                logging.debug(
                    f"file {current_file} does not exist, downloading from {os.getenv('DATA_FOLDER_PATH')}"
                )
                self._bucketRepository.download_from(
                    bucket_name=os.getenv("DATA_FOLDER_PATH"),
                    object_name=f"{expl_id.data}/{file}",
                    destination_file_path=current_file,
                )
            to_return[file.replace(".csv", "")] = pd.read_csv(current_file)

        return to_return

    def load_file(self, file_path: str, bucket_name: str) -> pd.DataFrame:
        file: str = self._bucketRepository.download_from(
            object_name=file_path, bucket_name=bucket_name
        )
        return pd.read_csv(file)
