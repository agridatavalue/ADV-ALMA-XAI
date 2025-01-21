import os
import logging
import pandas as pd

from ..repository.BucketRepository import BucketRepository
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class DataLoaderService:
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
