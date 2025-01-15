import os
import json
import logging
import pandas as pd
from os import path

from ..Helper import Helper
from ...domain.model.ModelMetaData import ModelMetaData
from ..repository.BucketRepository import BucketRepository
from ...domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
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

        x_file_path: str = f"{expl_id.model}/{expl_id.data}/x.csv"
        y_file_path: str = f"{expl_id.model}/{expl_id.data}/y.csv"

        bucket_name = os.getenv("DATA_FOLDER_PATH")
        if not os.path.exists(expl_id.get_data_locale_filepath()):
            logging.debug(
                f"file {x_file_path} does not exist, downloading from {bucket_name}"
            )
            file_x: str = self._bucketRepository.download_from(
                bucket_name=bucket_name,
                object_name=x_file_path,
                destination_file_path="x.csv",
            )

        if not Helper.is_local_path(y_file_path):
            logging.debug(
                f"file {y_file_path} does not exist, downloading from {bucket_name}"
            )
            file_y: str = self._bucketRepository.download_from(
                bucket_name=bucket_name,
                object_name=y_file_path,
                destination_file_path="y.csv",
            )

        data = {"x": pd.read_csv(file_x), "y": pd.read_csv(file_y)}
        os.remove(file_x)
        os.remove(file_y)

        return data

    def load_file(self, file_path: str, bucket_name: str) -> pd.DataFrame:
        file: str = self._bucketRepository.download_from(
            object_name=file_path,
            bucket_name=bucket_name,
        )
        return pd.read_csv(file)

    def load_explainer_metadata(
        self, expl_id: ExplainerIdentifier
    ) -> ExplainerMetaData:
        assert isinstance(
            expl_id, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        file: str = self._bucketRepository.download_from(
            object_name=expl_id.get_metadata_path(),
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
        )
        with open(file, "r") as json_file:
            metadata = json.load(json_file) or {}

        os.remove(file)
        return self._explainer_metadata_translator.translate(metadata)

    def load_model_metadata(
        self, explainer_identifier: ExplainerIdentifier
    ) -> ModelMetaData:
        assert isinstance(
            explainer_identifier, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        file: str = self._bucketRepository.download_from(
            object_name=explainer_identifier.metadata,
            bucket_name=os.getenv("MODEL_FOLDER_PATH"),
        )
        with open(file, "r") as json_file:
            metadata = json.load(json_file) or {}

        os.remove(file)
        return self._model_metadata_translator.translate(metadata)

    def upload(
        self,
        explainer_data: ExplainerMetaData,
        target: str,
        model_category: str,
        model_filename: str,
    ) -> str:
        assert isinstance(
            explainer_data, ExplainerMetaData
        ), Errors.EXPLAINER_DATA_NOT_EXPLAINER_METADATA

        if isinstance(explainer_data, ExplainerMetaData):
            filename: str = "metadata.json"
            model_path: str = os.getenv("EXPLAINER_FOLDER_PATH")

        temp_path: str = path.join(
            os.getenv("TEMP") or path.dirname(__file__), filename
        )
        with open(temp_path, "w") as file:
            file.write(json.dumps(explainer_data.to_dict()))

        res: str = self._bucketRepository.upload_to(
            bucket_name=model_path,
            local_filepath=temp_path,
            target_filepath=self.__calculate_explainer_path(
                target, model_category, filename, model_filename
            ),
        )
        os.remove(temp_path)
        return res

    def __calculate_explainer_path(
        self, target: str, model_category: str, filename: str, model_filename: str
    ):
        path_calc: str = path.join(
            model_filename, f"{target}_{model_category}", filename
        )
        return path_calc.lower().replace(" ", "_").replace("-", "_")
