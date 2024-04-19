from minio import Minio


class BucketRepository:
    _client: any
    bucketName: str

    def __init__(self, conf: dict) -> None:
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
            conf.get("endpoint"),
            access_key=conf.get("access_key"),
            secret_key=conf.get("secret_key"),
            secure=conf.get("secure", False),
            region=conf.get("region"),
        )
        self.bucketName = conf.get("bucketName")

    def downloadFrom(self, object_name: str, destination_file_path: str) -> str:
        if not destination_file_path:
            destination_file_path = object_name

        self.client.fget_object(self.bucket_name, object_name, destination_file_path)

        return destination_file_path
