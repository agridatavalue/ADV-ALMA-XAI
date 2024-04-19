import uvicorn
import multiprocessing
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

from src.adv_xai_fulfilment.presentation.TrainerPresentation import TrainerPresentation

app = FastAPI()


class uploadedmodel(BaseModel):
    model: str
    metadata: str
    pilot: str
    data: Optional[str] = None


@app.post("/build/")
def mapper(request: uploadedmodel):
    try:
        response = TrainerPresentation().train(
            request.model, request.pilot, request.metadata
        )
        return {
            "status": f"success - stored {len(response)} explainers and metadata in SECURESTOR"
        }
    except Exception as e:
        return {"status": e}


if __name__ == "__main__":
    multiprocessing.freeze_support()
    uvicorn.run("xai_builder:app", host="0.0.0.0", port=8005, reload=True)
