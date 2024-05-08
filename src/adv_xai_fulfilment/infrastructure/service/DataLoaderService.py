import os
import json
import pandas as pd

from ..repository.BucketRepository import BucketRepository


class DataLoaderService:
    _bucketRepository: BucketRepository

    def __init__(self) -> None:
        self._bucketRepository = BucketRepository(
            {"endpoint": "", "access_key": "", "secret_key": "", "bucket": ""}
        )

    def loadData(self, file_path: str):
        file_x: str = self._bucketRepository.downloadFrom(f"{file_path}/x.csv", "x.csv")
        file_y: str = self._bucketRepository.downloadFrom(f"{file_path}/y.csv", "y.csv")

        os.remove(file_x)
        os.remove(file_y)
        return {"x": pd.read_csv(file_x), "y": pd.read_csv(file_y)}

    def loadMetaData(self, metadata_path: str):
        file: str = self._bucketRepository.downloadFrom(metadata_path)
        with open(metadata_path, "r") as json_file:
            metadata = json.load(json_file)
        os.remove(file)
        return metadata
