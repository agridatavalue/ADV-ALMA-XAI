from typing import Optional

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
                "endpoint": os.getenv("STORE_ENDPOINT"),
                "access_key": os.getenv("STORE_ACCESS_KEY"),
                "secret_key": os.getenv("STORE_SECRET_KEY"),
                "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
            }
        )

    def load(
        self, expl_id: ExplainerIdentifier, data_type: DataType = DataType.TABULAR
    ) -> Optional[ModelData]:
        if data_type == DataType.TABULAR:
            return self.load_data(expl_id)
        elif data_type == DataType.IMAGE:
            return self.load_images(expl_id)

        raise ValueError(f"Data type {data_type} not supported")

    def load_data(self, expl_id: ExplainerIdentifier) -> Optional[ModelData]:
        if not expl_id.data:
            return

        logger.debug(f"loading data for {str(expl_id)}")
        bucket_name = os.getenv("DATA_FOLDER_PATH", '')
        
        data = ModelData()
        self._load_predict_data(data, bucket_name, expl_id)
        self._load_train_data(data, bucket_name, expl_id)
        return data
    
    def _load_train_data(self, data: ModelData, bucket_name: str, expl_id: ExplainerIdentifier) -> ModelData:
        if not expl_id.data_for_training:
            return data

        passed_folder_path: bool = self._bucketRepository.is_directory(bucket_name=bucket_name, path=expl_id.data_for_training)
        if not passed_folder_path:
            logger.debug(f"train data is a single file {expl_id.data_for_training}")
            self._bucketRepository.download_file_from(
                bucket_name=bucket_name,
                object_name=expl_id.data_for_training,
                destination_file_path=expl_id.get_data_locale_filepath(os.path.basename(expl_id.data_for_training)),
            )
            data.x_train = pd.read_csv(expl_id.get_data_locale_filepath(os.path.basename(expl_id.data_for_training)))
            return data
        
        # passed train data is a folder path, load all files in the folder  
        files: list[str] = self._bucketRepository.listdir(
            bucket_name=bucket_name, path=expl_id.data_for_training
        )
        
        logger.debug(f"train files to load: {files}")
        for file in files:
            current_file = expl_id.get_data_locale_filepath(file)
            os.makedirs(os.path.dirname(current_file), exist_ok=True)
            if not os.path.exists(current_file):
                logger.debug(
                    f"file {current_file} does not exist, downloading from {bucket_name}"
                )
                self._bucketRepository.download_from(
                    bucket_name=bucket_name,
                    object_name=f"{expl_id.data_for_training}/{file}" if passed_folder_path else expl_id.train_data,
                    destination_file_path=current_file,
                )
                
            file_extension = os.path.splitext(file)[1].lower()
            setattr(data, file.replace(file_extension, "")+'_train', pd.read_csv(current_file))

        return data

    def _load_predict_data(self, data: ModelData, bucket_name: str, expl_id: ExplainerIdentifier) -> ModelData:
        passed_folder_path: bool = self._bucketRepository.is_directory(bucket_name=bucket_name, path=expl_id.data)
        if not passed_folder_path:
            logger.debug(f"data is a single file {expl_id.data}")
            self._bucketRepository.download_file_from(
                bucket_name=bucket_name,
                object_name=expl_id.data,
                destination_file_path=expl_id.get_data_locale_filepath(os.path.basename(expl_id.data)),
            )
            data.x_predict = pd.read_csv(expl_id.get_data_locale_filepath(os.path.basename(expl_id.data)))
            return data
        
        # passed data is a folder path, load all files in the folder  
        files: list[str] = self._bucketRepository.listdir(
            bucket_name=bucket_name, path=expl_id.data
        )
        
        logger.debug(f"files to load: {files}")
        for file in files:
            current_file = expl_id.get_data_locale_filepath(file)
            os.makedirs(os.path.dirname(current_file), exist_ok=True)
            if not os.path.exists(current_file):
                logger.debug(
                    f"file {current_file} does not exist, downloading from {bucket_name}"
                )
                self._bucketRepository.download_from(
                    bucket_name=bucket_name,
                    object_name=f"{expl_id.data}/{file}" if passed_folder_path else expl_id.data,
                    destination_file_path=current_file,
                )
                
            file_extension = os.path.splitext(file)[1].lower()
            setattr(data, file.replace(file_extension, "")+'_predict', pd.read_csv(current_file))

        return data

    def load_images(self, expl_id: ExplainerIdentifier) -> list[ModelData]:
        if not expl_id.data:
            return []

        logger.info(f"loading images for {str(expl_id)}")

        result = []
        for file in self._bucketRepository.listdir(
            bucket_name=os.getenv("DATA_FOLDER_PATH", ''), path=expl_id.data
        ):
            current_file: str = expl_id.get_data_locale_filepath(file)
            if not os.path.exists(current_file):
                os.makedirs(os.path.dirname(current_file), exist_ok=True)
                current_file = self._bucketRepository.download_from(
                    bucket_name=os.getenv("DATA_FOLDER_PATH", ''),
                    object_name=f"{expl_id.data}/{file}",
                    destination_file_path=current_file,
                )

            data = ModelData()
            data._image_path = current_file
            result.append(data)

        return result
