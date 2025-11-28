import os

from src.adv_xai_fulfilment.infrastructure.repository.bucket_repository import BucketRepository

class KpiDataService:
    def __init__(self) -> None:
        self._bucket_repository = BucketRepository(
            {
                "endpoint": os.getenv("STORE_ENDPOINT"),
                "access_key": os.getenv("STORE_ACCESS_KEY"),
                "secret_key": os.getenv("STORE_SECRET_KEY"),
                "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
            }
        )

    def get_model_feedback(self, request: dict = {}):
        downloaded_files: list[str] = []
        model_name: str = request.get('model', '')
        bucket_name: str = os.getenv("EXPLAINER_FOLDER_PATH", "")
        
        destination_folder = os.path.join(os.getenv("TEMP", "/tmp"), "kpi_feedback", model_name)
        os.makedirs(destination_folder, exist_ok=True)
        
        all_content = list(self._bucket_repository._client.list_objects(
            bucket_name = bucket_name.rstrip('/'), 
            # prefix=model_name+'/',
            recursive = True
        ))
        print(f">>>", [c.object_name for c in all_content])
        
        for dir in self._bucket_repository.listdir(bucket_name=bucket_name, path=model_name):
            print(f"Checking directory: {dir}")
            if not self._bucket_repository.is_directory(bucket_name=bucket_name, path=dir):
                continue
            
            for partner_dir in self._bucket_repository.listdir(bucket_name=bucket_name, path=dir):
                if not self._bucket_repository.is_directory(bucket_name=bucket_name, path=partner_dir):
                    continue
                
                metadata_to_download: str = f"{model_name}/{partner_dir}/metadata.json"
                local_metadata_path: str = os.path.join(destination_folder, f"{partner_dir}-metadata.json")
                print(f"Downloading {metadata_to_download} to {local_metadata_path}")
                self._bucket_repository.download_from(
                    bucket_name=bucket_name,
                    object_name=metadata_to_download,
                    destination_file_path=local_metadata_path,
                )
                downloaded_files.append(local_metadata_path)
        
        return downloaded_files