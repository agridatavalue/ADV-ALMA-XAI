import os
import pandas as pd

from logger import get_logger
from ..repository import BucketRepository
from ...domain.model.data_type import DataType
from ...domain.model.model_data import ModelData
from ...domain.model.explainer_identifier import ExplainerIdentifier

logger = get_logger()

class DataLoaderService:
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

    def load(
        self, expl_id: ExplainerIdentifier, data_type: DataType = DataType.TABULAR
    ) -> ModelData:
        if data_type == DataType.TABULAR:
            return self.load_data(expl_id)
        elif data_type == DataType.IMAGE:
            return self.load_images(expl_id)

        raise ValueError(f"Data type {data_type} not supported")

    def load_data(self, expl_id: ExplainerIdentifier) -> ModelData:
        if not expl_id.data:
            return None

        logger.debug(f"loading data for {str(expl_id)}")

        data = ModelData()
        if os.path.exists(expl_id.get_data_locale_filepath('')):
            files = os.listdir(expl_id.get_data_locale_filepath(''))
        else:
            files = self._bucketRepository.listdir(
                bucket_name=os.getenv("DATA_FOLDER_PATH"), path=expl_id.data
            )
        
        logger.debug(f"files to load: {files}")
        for file in files:
            current_file = expl_id.get_data_locale_filepath(file)
            os.makedirs(os.path.dirname(current_file), exist_ok=True)
            if not os.path.exists(current_file):
                logger.debug(
                    f"file {current_file} does not exist, downloading from {os.getenv('DATA_FOLDER_PATH')}"
                )
                self._bucketRepository.download_from(
                    bucket_name=os.getenv("DATA_FOLDER_PATH"),
                    object_name=f"{expl_id.data}/{file}",
                    destination_file_path=current_file,
                )
            setattr(data, file.replace(".csv", ""), pd.read_csv(current_file))

        return data

    def load_images(self, expl_id: ExplainerIdentifier) -> list[ModelData]:
        if not expl_id.data:
            return []

        logger.info(f"loading images for {str(expl_id)}")

        result = []
        for file in self._bucketRepository.listdir(
            bucket_name=os.getenv("DATA_FOLDER_PATH"), path=expl_id.data
        ):
            current_file: str = expl_id.get_data_locale_filepath(file)
            if not os.path.exists(current_file):
                os.makedirs(os.path.dirname(current_file), exist_ok=True)
                current_file = self._bucketRepository.download_from(
                    bucket_name=os.getenv("DATA_FOLDER_PATH"),
                    object_name=f"{expl_id.data}/{file}",
                    destination_file_path=current_file,
                )

            data = ModelData()
            data._image_path = current_file
            result.append(data)

        return result
