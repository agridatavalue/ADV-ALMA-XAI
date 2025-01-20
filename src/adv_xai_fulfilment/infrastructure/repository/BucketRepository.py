import os
import shutil
from minio import Minio


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
            endpoint=conf.get("endpoint"),
            access_key=conf.get("access_key"),
            secret_key=conf.get("secret_key"),
            secure=conf.get("secure", True),
            region=conf.get("region"),
        )

    def download_from(
        self, bucket_name: str, object_name: str, destination_file_path: str = None
    ) -> str:
        if not destination_file_path:
            destination_file_path = object_name

        res = self._client.fget_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=object_name,
        )
        return shutil.move(res.object_name, destination_file_path)

    def upload_to(
        self, bucket_name: str, target_filepath: str, local_filepath: str
    ) -> str:
        result = self._client.fput_object(
            bucket_name=bucket_name,
            file_path=local_filepath,
            object_name=target_filepath.replace(os.sep, "/"),
        )
        return result.object_name
