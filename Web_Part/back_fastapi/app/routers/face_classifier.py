import os
import time
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from fastapi.param_functions import Depends
from typing import List, Optional

from models.efficientnet.efficientnet_model import load_model, get_prediction, convert_image
from back_fastapi.app.utils import ref_actor_image
from logger import get_ml_logger

router = APIRouter(
    prefix="/actorclass",
    tags=["classification"],
)

####################################
from pathlib import Path

here = Path(__file__)
# config_yaml_path = os.path.join(here.parents[2], "config.yaml")
config_yaml_path = "config.yaml"

logger = get_ml_logger(
    config_path=config_yaml_path,
    credential_json_path="./online_logger_test.json", # FIXME
    table_ref="tensile-stack-350418.bitcoin_logs.final_project", 
)
####################################

class InferenceResult(BaseModel):
    name: str
    ref_actor: Optional[str]
    percentage : float

    class Config:
        arbitrary_types_allowed = True


@router.post("/")
async def inference(files: List[UploadFile] = File(...), model=Depends(load_model)):
    
    model.eval()
    product = ''
    # for file in files:
    image_bytes = await files[0].read()
    
    start = time.time() # start time for checking inference time!
    predicted, percentage = get_prediction(model=model, image_bytes=image_bytes)
    ref_actor, inference_result = ref_actor_image(predicted)
    product = InferenceResult(name=inference_result,ref_actor = ref_actor, percentage=percentage)
    # print(f"{time.time() - start:.5f}")
    # inference_time = f"{time.time() - start:.5f}"
    logger.info(f"Classification Inference : {time.time() - start:.5f}") # classification inference time
    
    return product

class DetectResult(BaseModel):
    num_box : int
    result: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True


@router.post("/detect")
async def detect(files: List[UploadFile] = File(...)):

    # for file in files:
    image_bytes = await files[0].read()
    len_boxes, converted_image = convert_image(image_bytes=image_bytes)
    product = DetectResult(num_box = len_boxes, result=[converted_image])
    return product