import os
import json
import pickle
import pandas as pd

from ..repository.BucketRepository import BucketRepository
from src.adv_xai_fulfilment.domain.model.Model import Model


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

    def loadModelFrom(self, model_path: str) -> Model:
        file: str = self._bucketRepository.downloadFrom(model_path)

        with open(model_path, "rb") as file:
            model: dict = pickle.load(file)

        os.remove(file)
        return Model(
            name=model.get("name"),
            type=model.get("type"),
            category=model.get("category"),
            data_type=model.get("data_type"),
            explanations=model.get("explanations"),
            is_distributed=model.get("is_distributed"),
            train_set_required=model.get("train_set_required"),
            has_categorical_features=model.get("has_categorical_features"),
        )

    def loadMetaData(self, metadata_path: str):
        file: str = self._bucketRepository.downloadFrom(metadata_path)
        with open(metadata_path, "r") as json_file:
            metadata = json.load(json_file)
        os.remove(file)
        return metadata
