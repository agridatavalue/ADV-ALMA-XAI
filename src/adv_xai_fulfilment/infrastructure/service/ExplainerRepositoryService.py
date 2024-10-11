import os
import pickle

from ..repository.BucketRepository import BucketRepository
from ...domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.infrastructure.Constants import Errors


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

    def __get_filename(self, explainer: Explainer) -> str:
        return f"{explainer.name}.pkl"

    def download(self, pilot: str, explainer: Explainer) -> str:
        destination_file_path: str = os.path.join(
            os.getenv("temp"), f"explainer_{pilot}_{explainer.name}.pkl"
        )
        self._bucketRepository.download_from(
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
            object_name=f"{pilot}/{self.__get_filename(explainer)}",
            destination_file_path=destination_file_path,
        )

        return destination_file_path if os.path.exists(destination_file_path) else ""

    def upload_to(self, explainer: Explainer, pilot: str, model_path: str):
        assert isinstance(explainer, Explainer), Errors.EXPLAINER_NOT_EXPLAINER

        explainer_filename: str = self.__get_filename(explainer)
        with open(explainer_filename, "wb") as file:
            pickle.dump(explainer.build_result, file)

        self._bucketRepository.upload_to(
            bucket_name=model_path,
            local_filepath=explainer_filename,
            target_filepath=os.path.join(pilot, explainer_filename),
        )
        os.remove(explainer_filename)
