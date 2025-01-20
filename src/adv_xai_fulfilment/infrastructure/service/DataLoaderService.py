import os
import json
import logging
import pandas as pd
from os import path

from ...domain.model.ModelMetaData import ModelMetaData
from ..repository.BucketRepository import BucketRepository
from ...domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
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
            metadata: dict = json.load(json_file) or {}

        return self._explainer_metadata_translator.translate(metadata)

    def load_model_metadata(
        self, explainer_identifier: ExplainerIdentifier
    ) -> ModelMetaData:
        assert isinstance(
            explainer_identifier, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        if not os.path.exists(explainer_identifier.get_metadata_locale_filepath()):
            file: str = self._bucketRepository.download_from(
                object_name=explainer_identifier.metadata_identifier,
                bucket_name=os.getenv("MODEL_FOLDER_PATH"),
            )

        with open(file, "r") as json_file:
            metadata: dict = json.load(json_file) or {}

        return self._model_metadata_translator.translate(metadata)

    def upload(
        self,
        explainer_data: ExplainerMetaData,
        explainer_identifier: ExplainerIdentifier,
    ) -> str:
        assert isinstance(
            explainer_data, ExplainerMetaData
        ), Errors.EXPLAINER_DATA_NOT_EXPLAINER_METADATA

        temp_path: str = explainer_identifier.get_metadata_locale_filepath()
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, "w") as file:
            file.write(json.dumps(explainer_data.to_dict()))

        return self._bucketRepository.upload_to(
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
            local_filepath=temp_path,
            target_filepath=explainer_identifier.get_metadata_path(),
        )
