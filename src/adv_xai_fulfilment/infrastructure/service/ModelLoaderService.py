import os
import pickle
import logging
from os import path

from ..repository.BucketRepository import BucketRepository
from src.adv_xai_fulfilment.domain.model.Model import Model
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.domain.service.ModelTranslator import ModelTranslator
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class ModelLoaderService:
    _model_translator: ModelTranslator
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
        self._model_translator = ModelTranslator()

    def load_from(self, model_file_path: str, meta_data: ModelMetaData) -> Model:
        logging.debug(f"loading model from {model_file_path}")

        model_file_path = Model.get_locale_filepath(model_file_path)
        if not path.exists(model_file_path):
            model_file_path: str = self._bucketRepository.download_from(
                object_name=model_file_path,
                bucket_name=os.getenv("MODEL_FOLDER_PATH"),
                destination_file_path=model_file_path,
            )

        logging.debug(
            f"select domain model for: framework {meta_data.framework} and algoritm {meta_data.algorithm}"
        )
        return (
            self._model_translator.with_(meta_data.framework)
            .and_(meta_data.algorithm)
            .translate(model_file_path)
        )

    def upload_explainer(
        self, explainer: Explainer, identifier: ExplainerIdentifier
    ) -> str:
        with open(explainer.file_name, "wb") as file:
            pickle.dump(explainer.build_result, file)

        object_name = self._bucketRepository.upload_to(
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
            local_filepath=explainer.file_name,
            target_filepath=identifier.get_filename_path(explainer.file_name),
        )
        os.remove(explainer.file_name)
        return object_name

    def upload_to(
        self,
        target: str,
        explainer: Explainer,
        model_path: str,
        model_category: str,
        model_filename: str,
    ):
        assert isinstance(explainer, Explainer), Errors.EXPLAINER_NOT_EXPLAINER

        with open(explainer.file_name, "wb") as file:
            pickle.dump(explainer.build_result, file)

        self._bucketRepository.upload_to(
            bucket_name=model_path,
            local_filepath=explainer.file_name,
            target_filepath=self.__calculate_explainer_path(
                target, model_category, explainer, model_filename
            ),
        )
        os.remove(explainer.file_name)

    def __calculate_explainer_path(
        self,
        target: str,
        model_category: str,
        explainer: Explainer,
        model_filename: str,
    ):
        path: str = os.path.join(
            model_filename, f"{target}_{model_category}", explainer.name + ".pkl"
        )
        return path.lower().replace(" ", "_").replace("-", "_")
