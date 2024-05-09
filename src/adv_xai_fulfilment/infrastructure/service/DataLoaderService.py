import os
import json
import pandas as pd

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
        file_x: str = self._bucketRepository.download_from(
            f"{file_path}/x.csv", "x.csv"
        )
        file_y: str = self._bucketRepository.download_from(
            f"{file_path}/y.csv", "y.csv"
        )

        data = {"x": pd.read_csv(file_x), "y": pd.read_csv(file_y)}
        os.remove(file_x)
        os.remove(file_y)

        return data

    def load_meta_data(self, metadata_path: str) -> dict:
        file: str = self._bucketRepository.download_from(metadata_path)
        with open(metadata_path, "r") as json_file:
            metadata = json.load(json_file)

        os.remove(file)
        return metadata
