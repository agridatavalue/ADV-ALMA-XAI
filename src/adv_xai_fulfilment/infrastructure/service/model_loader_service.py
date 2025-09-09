import os

from logger import get_logger
from ..repository import BucketRepository
from src.adv_xai_fulfilment.domain.model.model import Model
from src.adv_xai_fulfilment.domain.service import ModelTranslator
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier

logger = get_logger()

class ModelLoaderService:
    _model_translator: ModelTranslator
    _bucketRepository: BucketRepository

    def __init__(self, bucketRepository: BucketRepository = None):
        self._bucketRepository = bucketRepository or BucketRepository(
            {
                "endpoint": os.getenv("STORE_ENDPOINT"),
                "access_key": os.getenv("STORE_ACCESS_KEY"),
                "secret_key": os.getenv("STORE_SECRET_KEY"),
                "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
            }
        )
        self._model_translator = ModelTranslator()

    def load_from(self, expl_id:ExplainerIdentifier, meta_data: ModelMetaData) -> Model:
        assert isinstance(expl_id, ExplainerIdentifier), "expl_id must be an instance of ExplainerIdentifier"
        assert isinstance(meta_data, ModelMetaData), "meta_data must be an instance of ModelMetaData"

        model_local_file_path: str = expl_id.get_model_locale_filepath()
        logger.debug(f"loading model from {expl_id.model} to {model_local_file_path}")

        if not os.path.exists(model_local_file_path):
            model_local_file_path: str = self._bucketRepository.download_from(
                object_name=expl_id.model,
                bucket_name=os.getenv("MODEL_FOLDER_PATH", ""),
                destination_file_path=model_local_file_path,
            )

        logger.debug(
            f"select domain model for: framework {meta_data.framework} and algoritm {meta_data.algorithm}"
        )
        return (
            self._model_translator.with_(meta_data.framework)
            .and_(meta_data.algorithm)
            .translate(model_local_file_path)
        )
