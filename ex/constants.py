import os
from dotenv import load_dotenv

load_dotenv()

minio_endpoint = os.environ["MINIO_ENDPOINT"]
access_key = os.environ["MINIO_PUBLIC_KEY"]
secret_key = os.environ["MINIO_PRIVATE_KEY"]

minio_models = "models"
minio_explainers = "explanators"
minio_datasets = "syntheticdatasets"
