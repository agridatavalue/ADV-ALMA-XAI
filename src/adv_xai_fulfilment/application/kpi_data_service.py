import os
import json

from src.adv_xai_fulfilment.infrastructure.repository.bucket_repository import BucketRepository

class KpiDataService:
    def __init__(self) -> None:
        self._bucket_repository = BucketRepository.create_default()

    def get_model_feedback(self, request: dict = {}):
        downloaded_files: list[str] = []
        model_name: str = request.get('model', '')
        bucket_name: str = os.getenv("EXPLAINER_FOLDER_PATH", "")
        
        destination_folder = os.path.join(os.getenv("TEMP", "/tmp"), "kpi_feedback", model_name)
        os.makedirs(destination_folder, exist_ok=True)
        
        for file in self._bucket_repository.listdir(bucket_name=bucket_name, path='ai_flows/'+model_name+'/'):
            print(f"Checking file: {file}")
            if not file.endswith('feedback.json'):
                continue
            
            metadata_to_download: str = file
            local_metadata_path: str = os.path.join(destination_folder, f"{os.path.basename(os.path.dirname(file))}-feedback.json")
            print(f"Downloading {metadata_to_download} to {local_metadata_path}")
            self._bucket_repository.download_from(
                bucket_name=bucket_name,
                object_name=metadata_to_download,
                destination_file_path=local_metadata_path,
            )
            downloaded_files.append(local_metadata_path)
        
        num_of_feedback = 0
        num_of_positive_feedback = 0
        for feedback_file in downloaded_files:
            with open(feedback_file, 'r') as f:
                feedback_data: dict = json.load(f) or {}
                for partner_feedback in feedback_data.get('feedback', []):
                    for feedback in partner_feedback.get('feedback', []):
                        print(f"Feedback: {feedback}")
                        if not feedback.get('feedback'):
                            continue
                        
                        try:
                            feedback_value = int(feedback['feedback'])
                        except ValueError:
                            continue
                        
                        if feedback_value > 1: 
                            num_of_positive_feedback += 1
                        num_of_feedback += 1
                        
        return {
            "model_name": model_name,
            "num_of_feedback": num_of_feedback,
            "num_of_positive_feedback": num_of_positive_feedback,
            "percentage_positive_feedback": (
                num_of_positive_feedback / num_of_feedback * 100 if num_of_feedback > 0 else 0
            ),
        }