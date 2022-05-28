from fastapi import APIRouter, UploadFile, File
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from models.beautygan import get_beautygan, transfer
from back_fastapi.app.storage import upload_to_bucket, download_from_bucket
from back_fastapi.app.utils import from_image_to_bytes
import json, requests, random, base64, io
from PIL import Image



router = APIRouter(
    prefix="/beauty",
    tags=["beautygan"],
)
class Item(BaseModel):
    name: str = ''

class TransferImage(BaseModel):
    result: Optional[List[str]]

    # pydantic custom class 허용
    class Config:
        arbitrary_types_allowed = True


@router.post("/")
async def make_transfer(
    files: List[UploadFile] = [File(...)], 
    data:Item=Dict[str,str],
    model=Depends(get_beautygan)
):
    sess, graph = model
    with open('actor_data.json', 'r', encoding="UTF-8") as f:
        json_data = json.loads(f.read())
    print(data)
    class_actor = "공유"
    img_url = json_data[class_actor][random.randrange(0, 3)]

    image_bytes = await files[0].read() # user image
    ref_image = Image.open(requests.get(img_url, stream=True).raw)
    ref_bytes_str = from_image_to_bytes(ref_image)
    ref_bytes = base64.b64decode(ref_bytes_str)

    # np.ndarray -> PIL 이미지 -> ASCII코드로 변환된 bytes 데이터(str)
    transfer_result, transfer_refer = transfer(sess, graph, image_bytes, ref_bytes)
    product = TransferImage(result=[transfer_result, transfer_refer])

    return product
