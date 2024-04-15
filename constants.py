import os
from kubernetes import client, config

config.load_incluster_config()
api = client.CoreV1Api()
service = api.read_namespaced_service(name="securestore", namespace="agridatavalue")

minio_endpoint = service.spec.cluster_ip
access_key = os.environ["MINIO_PUBLIC_KEY"]
secret_key = os.environ["MINIO_PRIVATE_KEY"]
minio_models = os.environ["MINIO_MODELS"]
minio_explainers = os.environ["MINIO_EXPLAINERS"]
minio_datasets = os.environ["MINIO_DATASETS"]

