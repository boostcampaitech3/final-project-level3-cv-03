from fastapi import APIRouter, UploadFile, File
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from models.beautygan.beautygan_model import get_beautygan, transfer
from back_fastapi.app.storage import upload_to_bucket, download_from_bucket
from back_fastapi.app.utils import ref_actor_image
import base64, io
from PIL import Image

router = APIRouter(
    prefix="/beauty",
    tags=["beautygan"],
)
class Item(BaseModel):
    name: str

class TransferImage(BaseModel):
    result: Optional[List[str]]
    data: Optional[Item]
    # pydantic custom class 허용
    class Config:
        arbitrary_types_allowed = True

actor = ''
@router.post("/actor")
async def save_actor(
    actor_name:Item
):
    print('데이터',dict(actor_name)['name'])
    global actor
    actor = dict(actor_name)['name']
    return actor



@router.post("/")
async def make_transfer(
    files: List[UploadFile] = [File(...)], 
    model=Depends(get_beautygan)
):
    global actor
    sess, graph = model
    image_bytes = await files[0].read() # user image
    ref_bytes_test = await files[1].read() 

    ref_bytes_str = ref_actor_image(actor)
    ref_bytes = base64.b64decode(ref_bytes_str)

    # np.ndarray -> PIL 이미지 -> ASCII코드로 변환된 bytes 데이터(str)
    transfer_result, transfer_refer = transfer(sess, graph, image_bytes, ref_bytes_test)
    product = TransferImage(result=[transfer_result, transfer_refer])

    return product
