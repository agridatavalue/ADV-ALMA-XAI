import os
import pickle
import logging

from ..Helper import Helper
from ...domain.model.Model import Model
from ...domain.model.ModelMetaData import ModelMetaData
from ...domain.model.explainers.Explainer import Explainer
from ..repository.BucketRepository import BucketRepository
from ...domain.service.ModelTranslator import ModelTranslator
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from ..repository.PersistenceRepository import PersistenceRepository


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

    def upload_to(
        self,
        target: str,
        explainer: Explainer,
        model_path: str,
        model_category: str,
        model_filename: str,
    ):
        assert isinstance(explainer, Explainer), Errors.EXPLAINER_NOT_EXPLAINER

        explainer_filename: str = explainer.name + ".pkl"
        with open(explainer_filename, "wb") as file:
            pickle.dump(explainer.build_result, file)

        self._bucketRepository.upload_to(
            bucket_name=model_path,
            local_filepath=explainer_filename,
            target_filepath=self.__calculate_explainer_path(
                target, model_category, explainer, model_filename
            ),
        )
        os.remove(explainer_filename)

    def download_for(self, pilot: str):
        destination_file_path = os.path.join(os.getenv("temp"), f"pilot_{pilot}.pkl")
        self._bucketRepository.download_from(
            bucket_name="", object_name="", destination_file_path=destination_file_path
        )
        return []

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
