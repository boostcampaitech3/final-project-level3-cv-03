import os
import time
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from fastapi.param_functions import Depends
from typing import List, Optional

from models.efficientnet.efficientnet_model import load_model, get_prediction
from back_fastapi.app.utils import ref_actor_image
from Web_Part.logger import get_ml_logger

router = APIRouter(
    prefix="/actorclass",
    tags=["classification"],
)

####################################
from pathlib import Path

here = Path(__file__)
config_yaml_path = os.path.join(here.parents[2], "config.yaml")

logger = get_ml_logger(
    config_path=config_yaml_path,
    credential_json_path="./app/online-service-logger.json", # FIXME
    table_ref="tensile-stack-350418.online_serving_logs.inference_time", 
)
####################################

class InferenceResult(BaseModel):
    name: str
    ref_actor: Optional[str]

    class Config:
        arbitrary_types_allowed = True


@router.post("/")
async def inference(files: List[UploadFile] = File(...), model=Depends(load_model)):
    
    model.eval()
    product = ''
    # for file in files:
    image_bytes = await files[0].read()
    start = time.time() # start time for checking inference time!
    predicted = get_prediction(model=model, image_bytes=image_bytes)
    ref_actor, inference_result = ref_actor_image(predicted)
    product = InferenceResult(name=inference_result,ref_actor =ref_actor)
    logger.info(f"Classification Inference : {time.time() - start:.5f}") # classification inference time
    return product
