import os
import json
import shutil

from logger import get_logger
from ..constants import Errors
from ..repository import BucketRepository
from ...domain.model.model_metadata import ModelMetaData
from ...domain.model.explainer_metadata import ExplainerMetaData
from ...domain.model.explainer_identifier import ExplainerIdentifier
from .translator import ModelMetaDataTranslator, ExplainerMetaDataTranslator

logger = get_logger()

class MetaDataLoaderService:
    _bucketRepository: BucketRepository
    _model_metadata_translator: ModelMetaDataTranslator
    _explainer_metadata_translator: ExplainerMetaDataTranslator

    def __init__(self, bucket_repository: BucketRepository = None):
        self._bucketRepository = bucket_repository or BucketRepository(
            {
                "endpoint": os.getenv("STORE_ENDPOINT"),
                "access_key": os.getenv("STORE_ACCESS_KEY"),
                "secret_key": os.getenv("STORE_SECRET_KEY"),
                "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
            }
        )
        self._model_metadata_translator = ModelMetaDataTranslator()
        self._explainer_metadata_translator = ExplainerMetaDataTranslator()

    def load_explainer_metadata(self, expl_id: ExplainerIdentifier) -> ExplainerMetaData:
        assert isinstance(
            expl_id, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        file: str = expl_id.get_explainer_metadata_locale_filepath()
        if not os.path.exists(file):
            logger.debug(
                f"file {file} does not exist, downloading {expl_id.get_explainer_metadata_path()} from {os.getenv('EXPLAINER_FOLDER_PATH')}"
            )
            file: str = self._bucketRepository.download_from(
                object_name=expl_id.get_explainer_metadata_path(),
                bucket_name=os.getenv("EXPLAINER_FOLDER_PATH", ""),
                destination_file_path=file,
            )

        with open(file) as json_file:
            metadata: dict = json.load(json_file) or {}

        return self._explainer_metadata_translator.translate(metadata)

    def upload_explainer_metadata(
        self, expl_id: ExplainerIdentifier, metadata: ExplainerMetaData
    ) -> str:
        assert isinstance(
            metadata, ExplainerMetaData
        ), Errors.EXPLAINER_METADATA_NOT_EXPLAINER_METADATA
        assert isinstance(
            expl_id, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        file_path: str = expl_id.get_explainer_metadata_locale_filepath()
        with open(file_path, "w") as json_file:
            json.dump(metadata.to_dict(), json_file)

        return self._bucketRepository.upload_to(
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH", ""),
            target_filepath=expl_id.get_explainer_metadata_path(),
            local_filepath=file_path,
        )

    def load_model_metadata(self, expl_id: ExplainerIdentifier, force_download: bool = False) -> ModelMetaData:
        if not isinstance(expl_id, ExplainerIdentifier):
            raise ValueError(Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER)
        filepath: str = expl_id.get_model_metadata_locale_filepath()
        logger.debug(f"loading model metadata for {filepath} force_download={force_download}")

        if not os.path.exists(filepath) or force_download:
            if os.path.exists(expl_id.metadata_identifier):
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                shutil.copyfile(expl_id.metadata_identifier, filepath)
            else:
                logger.debug(
                    f'forced download for {os.getenv("MODEL_FOLDER_PATH", "")}/{expl_id.metadata_identifier}' if force_download else 
                    f'file {filepath} not exists, downloading {os.getenv("MODEL_FOLDER_PATH")}/{expl_id.metadata_identifier}' 
                )
                filepath: str = self._bucketRepository.download_from(
                    object_name=expl_id.metadata_identifier,
                    bucket_name=os.getenv("MODEL_FOLDER_PATH", ""),
                    destination_file_path=filepath,
                )

        with open(filepath) as json_file:
            metadata: dict = json.load(json_file) or {}

        return self._model_metadata_translator.translate(metadata)
