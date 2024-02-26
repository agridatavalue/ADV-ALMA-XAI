import multiprocessing
from multiprocessing import Manager
import subprocess
multiprocessing.set_start_method('fork', force=True)
from fastapi import FastAPI
import uvicorn
import os
from xai_functions import load_model, load_metadata, train_explanator
from minio import Minio
from constants import minio_endpoint, access_key, secret_key, minio_models, minio_explainers
from explainerdashboard import ClassifierExplainer, ExplainerDashboard,  RegressionExplainer
import dash_bootstrap_components as dbc
import schedule
import threading
from datetime import datetime
import time
from pydantic import BaseModel
import pandas as pd


app = FastAPI()

class uploadedmodel(BaseModel):
    model:str
    metadata:str
    pilot:str

class explainermodel(BaseModel):
    explainer:str
    #test_data:dict
     
running = dict()
port = 8006


@app.get("/xai/dashboard/")
def dashboard(item: explainermodel):
    global running, port
    client = Minio(minio_endpoint, access_key=access_key, secret_key=secret_key, secure=False)
    print(f"Searching objects in bucket {item.explainer}")
    objects = client.list_objects(minio_explainers, prefix=item.explainer, recursive=True)
    print("Found objects")
    objects = [obj.object_name for obj in objects]
    print(objects)
    if len(objects) != 2:
        return {"status": "error - explainer not found"}
    print("Downloading explainer and metadata")
    client.fget_object(minio_explainers, objects[0], objects[0])
    client.fget_object(minio_explainers, objects[1], objects[1])
    print("Loading metadata")
    metadata = load_metadata(objects[1])
    print("Searching for port")
    for port in range(8006, 8100):
        if port not in running.keys():
            break

    print("Starting dashboard")
    process = subprocess.Popen(["python", "dashboard_runner.py", str(port), objects[0]],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    print(f"Dashboard started on port {port}")
    running[port] = (process, datetime.now())
    return {"port": port}



def kill_old_dashboards():
    global running
    print(running)
    while True:
        print(running)
        now = datetime.now()
        print("Checking for old dashboards...")
        for port, (process, timestamp) in list(running.items()):
            print(f"Checking dashboard on port {port}")
            elapsed_time = (now - timestamp).total_seconds()
            print(f"Elapsed time: {elapsed_time}")
            if elapsed_time > 60:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except Exception as e:
                    print(f"Error while terminating process on port {port}: {e}")
                finally:
                    del running[port]
                    print(f"Dashboard on port {port} terminated after {elapsed_time} seconds.")
        time.sleep(1)

if __name__ == '__main__':
    uvicorn.run("xaibuilder:app", host="0.0.0.0", port=8005, reload=True)