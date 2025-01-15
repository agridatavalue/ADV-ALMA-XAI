import os
import json
import pandas as pd
from os import path

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
            object_name=expl_id.get_metadata_path(),
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
        )
        with open(file, "r") as json_file:
            metadata = json.load(json_file) or {}

        os.remove(file)
        return self._explainer_metadata_translator.translate(metadata)

    def load_model_metadata(self, expl_id: ExplainerIdentifier) -> ModelMetaData:
        assert isinstance(
            expl_id, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        file: str = expl_id.get_metadata_locale_filepath()
        if not path.exists(file):
            file: str = self._bucketRepository.download_from(
                object_name=expl_id.metadata.filename.lower(),
                bucket_name=os.getenv("MODEL_FOLDER_PATH"),
                destination_file_path=file,
            )

        with open(file, "r") as json_file:
            metadata = json.load(json_file) or {}

        return self._model_metadata_translator.translate(metadata)
