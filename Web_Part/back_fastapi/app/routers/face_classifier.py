from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from fastapi.param_functions import Depends
from typing import List, Optional

from models.efficientnet.efficientnet_model import load_model, get_prediction
from back_fastapi.app.utils import ref_actor_image

router = APIRouter(
    prefix="/actorclass",
    tags=["classification"],
)


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
    predicted, percentage = get_prediction(model=model, image_bytes=image_bytes)
    ref_actor, inference_result = ref_actor_image(predicted)
    product = InferenceResult(name=inference_result,ref_actor = ref_actor, percentage=percentage)
    
    return product
