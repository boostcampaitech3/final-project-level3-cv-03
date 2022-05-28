from fastapi import APIRouter
from fastapi import UploadFile, File
from pydantic import BaseModel
from fastapi.param_functions import Depends

from typing import List, Optional

from models.efficientnet import load_model, get_prediction


celeb_list = [
    "공유",
    "권나라",
    "문채원",
    "박하선",
    "배두나",
    "신민아",
    "신성록",
    "안재현",
    "여진구",
    "유아인",
    "이다희",
    "이병헌",
    "이선균",
    "이시영",
    "전미도",
    "정은지",
    "조정석",
    "차승원",
    "한선화",
    "현빈",
]


router = APIRouter(
    prefix="/actorclass",
    tags=["classification"],
)


class InferenceResult(BaseModel):
    name: str

    class Config:
        arbitrary_types_allowed = True


@router.post("/")
async def inference(files: List[UploadFile] = File(...), model=Depends(load_model)):
    
    model.eval()
    product = ''
    for file in files:
        image_bytes = await file.read()
        predicted = get_prediction(model=model, image_bytes=image_bytes)
        inference_result = celeb_list[predicted]
        product = InferenceResult(name=inference_result)

    return product
