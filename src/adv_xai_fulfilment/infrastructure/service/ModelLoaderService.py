import os
import pickle
import logging

from ..Helper import Helper
from ..repository.BucketRepository import BucketRepository
from src.adv_xai_fulfilment.domain.model.Model import Model
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from ..repository.PersistenceRepository import PersistenceRepository
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.domain.service.ModelTranslator import ModelTranslator
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class ModelLoaderService:
    _model_translator: ModelTranslator
    _bucketRepository: BucketRepository
    _persistenceRepository: PersistenceRepository

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
        self._persistenceRepository = PersistenceRepository()

    def load_from(self, model_file_path: str, meta_data: ModelMetaData) -> Model:
        logging.debug(f"loading model from {model_file_path}")

        if not Helper.is_local_path(model_file_path):
            logging.debug(
                f"is not a local path, downloading {model_file_path} from {os.getenv('MODEL_FOLDER_PATH')}"
            )
            model_file_path: str = self._bucketRepository.download_from(
                bucket_name=os.getenv("MODEL_FOLDER_PATH"), object_name=model_file_path
            )

        selected_model: Model = (
            self._model_translator.with_(meta_data.framework)
            .and_(meta_data.algorithm)
            .translate(model_file_path)
        )

        os.remove(model_file_path)
        return selected_model

    def upload_explainer(self, explainer: Explainer, identifier: ExplainerIdentifier):
        with open(explainer.file_name, "wb") as file:
            pickle.dump(explainer.build_result, file)

        self._bucketRepository.upload_to(
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
            local_filepath=explainer.file_name,
            target_filepath=identifier.get_filename_path(explainer.file_name),
        )
        os.remove(explainer.file_name)

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
