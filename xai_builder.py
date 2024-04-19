import os
import uvicorn
import pandas as pd
import multiprocessing
from minio import Minio
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from xai_functions import load_model, load_metadata, train_explanator
from constants import (
    minio_endpoint,
    access_key,
    secret_key,
    minio_models,
    minio_explainers,
    minio_datasets,
)


app = FastAPI()
running = dict()


class uploadedmodel(BaseModel):
    model: str
    metadata: str
    pilot: str
    data: Optional[str] = None


@app.post("/build/")
def mapper(item: uploadedmodel):
    client = Minio(
        minio_endpoint, access_key=access_key, secret_key=secret_key, secure=False
    )
    print(item.model)
    client.fget_object(minio_models, item.model, item.model)

    model = load_model(item.model)
    # Load metadata
    client.fget_object(minio_models, item.metadata, item.metadata)
    metadata = load_metadata(item.metadata)
    # delete the files
    os.remove(item.model)
    os.remove(item.metadata)

    # train explainer
    data = None
    if item.data:
        client.fget_object(minio_datasets, f"{item.data}/x.csv", "x.csv")
        client.fget_object(minio_datasets, f"{item.data}/y.csv", "y.csv")
        data = {"x": pd.read_csv("x.csv"), "y": pd.read_csv("y.csv")}

    explainers = train_explanator(model, metadata, data)
    # delete data
    if item.data:
        os.remove("x.csv")
        os.remove("y.csv")

    print(explainers)
    for filename, json_filename in explainers:
        model_path = item.pilot + "/" + "".join(filename.split("/")[1:])
        metadata_path = item.pilot + "/" + "".join(json_filename.split("/")[1:])
        client.fput_object(minio_explainers, model_path, filename)
        client.fput_object(minio_explainers, metadata_path, json_filename)
        # delete the files
        os.remove(filename)
        os.remove(json_filename)

    return {
        "status": f"success - stored {len(explainers)} explainers and metadata in SECURESTOR"
    }


if __name__ == "__main__":
    multiprocessing.freeze_support()
    uvicorn.run("xai_builder:app", host="0.0.0.0", port=8005, reload=True)
