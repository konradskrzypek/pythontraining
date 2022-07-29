from typing import Optional
from uuid import UUID

from fastapi import FastAPI, UploadFile, Depends, File
from mlserver.datasets import DatasetService
from mlserver.ml.model import MlService

app = FastAPI()


# @app.get("/models/{id}")
# @app.get("/models/{id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     model_repository.getById(item_id)
#     return {"item_id": item_id, "q": q}


@app.post("/datasets/{dataset_id}")
def upload_dataset_version(dataset_id: UUID, dataset: UploadFile = File(...), dataset_service: DatasetService = Depends()):
    version_id = dataset_service.persist(dataset_id, dataset)
    return {"dataset_id": dataset_id, "version_id": version_id}


@app.post("/datasets")
def upload_dataset(dataset: UploadFile = File(...), dataset_service: DatasetService = Depends()):
    dataset_id, version_id = dataset_service.persist_new(dataset)
    return {"dataset_id": dataset_id, "version_id": version_id}


@app.get("/datasets/{dataset_id}/{version_id}")
def read_dataset(dataset_id: UUID, version_id: int, dataset_service: DatasetService = Depends()):
    dataset = dataset_service.get_by_id_and_version(dataset_id, version_id)
    return dataset.dataset_data


@app.post("/models/train/{dataset_id}/{version_id}")
def train_model(dataset_id: UUID, version_id: int, ml_service: MlService = Depends()):
    model_id, model_version_id = ml_service.train_new(dataset_id, version_id)
    return {"model_id": model_id, "version_id": version_id}
