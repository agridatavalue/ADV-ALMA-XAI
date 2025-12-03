import os
import shutil
from minio import Minio

from logger import get_logger

logger = get_logger()


class BucketRepository:
    _client: Minio

    def __init__(self, conf: dict):
        """
        conf param be like:
            - endpoint   [string] (Required)
            - access_key [string] (Required)
            - secret_key [string] (Required)
            - bucketName [string] (Required)
            - secure     [  bool] (Optional)
            - region     [string] (Optional)
        """
        self._client = Minio(
            endpoint=conf.get("endpoint", "") or "",
            access_key=conf.get("access_key"),
            secret_key=conf.get("secret_key"),
            secure=conf.get("secure", True),
            region=conf.get("region"),
        )

    def listdir(self, bucket_name: str, path: str) -> list[str]:
        return [
            (obj.object_name or "").replace(path + "/", "")
            for obj in self._client.list_objects(
                bucket_name = bucket_name.rstrip('/'), 
                prefix = path+'/' if not path.endswith('/') else path, 
                recursive = True
            ) if obj
        ]
        
    def is_directory(self, bucket_name: str, path: str) -> bool:
        objects = self._client.list_objects(
            bucket_name = bucket_name.rstrip('/'), 
            prefix = path+'/' if not path.endswith('/') else path, 
            recursive = True
        )
        for obj in objects:
            if obj and (obj.object_name or "") != path.rstrip('/'):
                return True
        return False

    def download_from(
        self, bucket_name: str, object_name: str, destination_file_path: str = ""
    ) -> str:
        if not object_name:
            raise ValueError("object_name must be provided")
        
        logger.debug(f"Downloading {object_name} from bucket {bucket_name}")
        if not destination_file_path:
            destination_file_path = object_name

        res = self._client.fget_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=object_name,
        )

        if destination_file_path and os.path.dirname(destination_file_path):
            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
        return shutil.move(res.object_name, destination_file_path) # type: ignore
    
    def download_file_from(self, bucket_name: str, object_name: str, destination_file_path: str) -> str:
        if destination_file_path and os.path.dirname(destination_file_path):
            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
            
        self._client.fget_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=destination_file_path,
        )
        return destination_file_path

    def upload_to(
        self, bucket_name: str, target_filepath: str, local_filepath: str
    ) -> str:
        result = self._client.fput_object(
            bucket_name=bucket_name,
            file_path=local_filepath,
            object_name=target_filepath.replace(os.sep, "/"),
        )
        return result.object_name
    
    @staticmethod
    def create_default() -> "BucketRepository":
        return BucketRepository(
            {
                "endpoint": os.getenv("STORE_ENDPOINT"),
                "access_key": os.getenv("STORE_ACCESS_KEY"),
                "secret_key": os.getenv("STORE_SECRET_KEY"),
                "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
            }
        )
