import os
import json
import pickle
import logging

from ..repository import BucketRepository
from ...domain.model.explainers import Explainer
from ...domain.model.explainers.explainer import Explainer
from ...domain.model.explainer_metadata import ExplainerMetaData
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from ...domain.model.explainer_identifier import ExplainerIdentifier


class ExplainerRepositoryService:
    _bucketRepository: BucketRepository

    def __init__(self):
        self._bucketRepository = BucketRepository(
            {
                "endpoint": os.getenv("MINIO_ENDPOINT"),
                "access_key": os.getenv("MINIO_ACCESS_KEY"),
                "secret_key": os.getenv("MINIO_SECRET_KEY"),
            }
        )

    def download_from(
        self,
        explainer: Explainer,
        explainer_identifier: ExplainerIdentifier,
    ) -> str:
        logging.debug(f"loading explainer {explainer.name}")
        destination_file_path: str = explainer_identifier.get_explainer_locale_filepath(
            explainer
        )

        if not os.path.exists(destination_file_path):
            self._bucketRepository.download_from(
                bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
                object_name=explainer_identifier.get_filename_path(explainer.file_name),
                destination_file_path=destination_file_path,
            )
        return destination_file_path if os.path.exists(destination_file_path) else ""

    def upload_to(self, explainer: Explainer, identifier: ExplainerIdentifier) -> str:
        assert isinstance(explainer, Explainer), Errors.EXPLAINER_NOT_EXPLAINER
        logging.debug(f"uploading the explainer {explainer.name}")

        locale_explainer_path: str = identifier.get_explainer_locale_filepath(explainer)

        os.makedirs(os.path.dirname(locale_explainer_path), exist_ok=True)
        with open(locale_explainer_path, "wb") as file:
            pickle.dump(explainer.build_result, file)

        return self._bucketRepository.upload_to(
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
            local_filepath=locale_explainer_path,
            target_filepath=identifier.get_filename_path(explainer.file_name),
        )

    def upload_metadata(
        self, expl_id: ExplainerIdentifier, metadata: ExplainerMetaData
    ) -> str:
        assert isinstance(
            metadata, ExplainerMetaData
        ), Errors.EXPLAINER_METADATA_NOT_EXPLAINER_METADATA

        os.makedirs(os.path.join(os.getenv("TEMP"), expl_id.model), exist_ok=True)
        metadata_filename: str = os.path.join(
            os.getenv("TEMP"), expl_id.model, "metadata.json"
        )
        with open(metadata_filename, "w") as file:
            json.dump(metadata.to_dict(), file)

        return self._bucketRepository.upload_to(
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
            local_filepath=metadata_filename,
            target_filepath=metadata.get_file_path(expl_id),
        )
