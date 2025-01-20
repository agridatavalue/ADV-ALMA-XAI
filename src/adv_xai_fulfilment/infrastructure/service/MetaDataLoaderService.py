import os
import json
import logging
import pandas as pd

from ...domain.model.ModelMetaData import ModelMetaData
from ..repository.BucketRepository import BucketRepository
from ...domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from .translator.ModelMetaDataTranslator import ModelMetaDataTranslator
from .translator.ExplainerMetaDataTranslator import ExplainerMetaDataTranslator
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class MetaDataLoaderService:
    _bucketRepository: BucketRepository
    _model_metadata_translator: ModelMetaDataTranslator
    _explainer_metadata_translator: ExplainerMetaDataTranslator

    def __init__(self, bucket_repository: BucketRepository = None):
        self._bucketRepository = bucket_repository or BucketRepository(
            {
                "endpoint": os.getenv("MINIO_ENDPOINT"),
                "access_key": os.getenv("MINIO_ACCESS_KEY"),
                "secret_key": os.getenv("MINIO_SECRET_KEY"),
                "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
            }
        )
        self._model_metadata_translator = ModelMetaDataTranslator()
        self._explainer_metadata_translator = ExplainerMetaDataTranslator()

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
            object_name=expl_id.get_explainer_metadata_path(),
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
        )
        with open(file, "r") as json_file:
            metadata = json.load(json_file) or {}

        return self._explainer_metadata_translator.translate(metadata)

    def upload_explainer_metadata(
        self, expl_id: ExplainerIdentifier, metadata: ExplainerMetaData
    ):
        assert isinstance(
            metadata, ExplainerMetaData
        ), Errors.EXPLAINER_METADATA_NOT_EXPLAINER_METADATA
        assert isinstance(
            expl_id, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        file_path: str = metadata.get_locale_file_path(expl_id)
        with open(file_path, "w") as json_file:
            json.dump(metadata.to_dict(), json_file)

        return self._bucketRepository.upload_to(
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
            target_filepath=metadata.get_file_path(expl_id),
            local_filepath=file_path,
        )

    def load_model_metadata(self, expl_id: ExplainerIdentifier) -> ModelMetaData:
        assert isinstance(
            expl_id, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        filepath: str = expl_id.get_model_metadata_locale_filepath()
        if not os.path.exists(filepath):
            logging.debug(
                f'file {filepath} not exists, downloading {os.getenv("MODEL_FOLDER_PATH")}/{expl_id.metadata_identifier}'
            )
            filepath: str = self._bucketRepository.download_from(
                object_name=expl_id.metadata_identifier,
                bucket_name=os.getenv("MODEL_FOLDER_PATH"),
                destination_file_path=filepath,
            )

        with open(filepath, "r") as json_file:
            metadata: dict = json.load(json_file) or {}

        return self._model_metadata_translator.translate(metadata)
