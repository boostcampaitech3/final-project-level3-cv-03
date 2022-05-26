from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.param_functions import Depends
from pydantic import BaseModel
from typing import List,Optional
from back_fastapi.app.model import get_beautygan, transfer
from back_fastapi.app.storage import upload_to_bucket, download_from_bucket

router = APIRouter(
    prefix="/beauty",
    tags = ["beautygan"],
)

class TransferImage(BaseModel):
    result: Optional[List[str]]

    # pydantic custom class 허용
    class Config:
        arbitrary_types_allowed = True


@router.post("/")
async def make_transfer(files: List[UploadFile] = File(...), model=Depends(get_beautygan)):
    sess, graph = model
    image_bytes, ref_bytes = await files[0].read(), await files[1].read()
    
    # np.ndarray -> PIL 이미지 -> ASCII코드로 변환된 bytes 데이터(str)
    transfer_result = transfer(sess, graph, image_bytes, ref_bytes)
    product = TransferImage(result=[transfer_result, transfer_result])

    return product

