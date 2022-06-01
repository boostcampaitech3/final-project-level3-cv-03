import os
import time
from fastapi import APIRouter, UploadFile, File
from fastapi.param_functions import Depends
from pydantic import BaseModel
from typing import List, Optional
from models.beautygan.beautygan_model import get_beautygan, transfer
import base64, io

from Web_Part.logger import get_ml_logger

router = APIRouter(
    prefix="/beauty",
    tags=["beautygan"],
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

class TransferImage(BaseModel):
    result: Optional[List[str]]
    # pydantic custom class 허용
    class Config:
        arbitrary_types_allowed = True

@router.post("/")
async def make_transfer(
    files: List[UploadFile] = [File(...)], 
    model=Depends(get_beautygan)
):
    sess, graph = model
    image_bytes = await files[0].read() # user image
    ref_bytes = await files[1].read() # refer image

    start = time.time() # start time for checking inference time!

    # np.ndarray -> PIL 이미지 -> ASCII코드로 변환된 bytes 데이터(str)
    transfer_result, transfer_refer = transfer(sess, graph, image_bytes, ref_bytes)
    product = TransferImage(result=[transfer_result, transfer_refer])

    logger.info(f"BeautyGAN Inference : {time.time() - start:.5f}") # beautygan inference time
    return product
