import os

minio_address = os.environ["MINIO_ENDPOINT"]
minio_port = os.environ["MINIO_PORT"]
minio_endpoint = f"{minio_address}:{minio_port}"

access_key = os.environ["MINIO_PUBLIC_KEY"]
secret_key = os.environ["MINIO_PRIVATE_KEY"]
minio_models = "models"
minio_explainers = "explanators"
