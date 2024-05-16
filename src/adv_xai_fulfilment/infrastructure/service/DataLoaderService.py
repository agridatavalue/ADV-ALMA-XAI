import os
import json
import logging
import pandas as pd

from ..Helper import Helper
from ..repository.BucketRepository import BucketRepository


class DataLoaderService:
    _bucketRepository: BucketRepository

    def __init__(self) -> None:
        self._bucketRepository = BucketRepository(
            {
                "endpoint": os.getenv("MINIO_ENDPOINT"),
                "access_key": os.getenv("MINIO_ACCESS_KEY"),
                "secret_key": os.getenv("MINIO_SECRET_KEY"),
            }
        )

    def load_data(self, file_path: str) -> dict[str, pd.DataFrame]:
        if not file_path:
            return None

        x_file_path: str = os.path.join(file_path, "x.csv")
        y_file_path: str = os.path.join(file_path, "y.csv")

        if not Helper.is_local_path(x_file_path):
            logging.debug(
                f"is not a local path, downloading {x_file_path} from {os.getenv('MODEL_FOLDER_PATH')}"
            )
            file_x: str = self._bucketRepository.download_from(
                bucket_name=os.getenv("DATA_FOLDER_PATH"),
                object_name=x_file_path,
                destination_file_path="x.csv",
            )

        if not Helper.is_local_path(y_file_path):
            logging.debug(
                f"is not a local path, downloading {y_file_path} from {os.getenv('MODEL_FOLDER_PATH')}"
            )
            file_y: str = self._bucketRepository.download_from(
                bucket_name=os.getenv("DATA_FOLDER_PATH"),
                object_name=y_file_path,
                destination_file_path="y.csv",
            )

        data = {"x": pd.read_csv(file_x), "y": pd.read_csv(file_y)}
        os.remove(file_x)
        os.remove(file_y)

        return data

    def load_meta_data(self, metadata_filepath: str) -> dict:
        if not Helper.is_local_path(metadata_filepath):
            logging.debug(
                f"is not a local path, downloading {metadata_filepath} from {os.getenv('MODEL_FOLDER_PATH')}"
            )
            file: str = self._bucketRepository.download_from(
                object_name=metadata_filepath,
                bucket_name=os.getenv("MODEL_FOLDER_PATH"),
            )

        with open(file, "r") as json_file:
            metadata = json.load(json_file)

        os.remove(file)
        return metadata
