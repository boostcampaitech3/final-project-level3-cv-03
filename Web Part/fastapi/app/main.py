from ast import Bytes, Str
from fastapi import FastAPI, UploadFile, File
from fastapi.param_functions import Depends
from numpy import product
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List, Union, Optional, Dict, Any


from app.model import get_beautygan, transfer

app = FastAPI()


@app.get("/")
def hello_world():
    return {" Back : FastAPI & Front : Streamlit"}


class TransferImage(BaseModel):
    result: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True


@app.post("/order")
async def make_transfer(files: List[UploadFile] = File(...), model=Depends(get_beautygan)):

    # return {"Files" : files[0].file.read()}

    sess, graph = model
    image_bytes, ref_bytes = await files[0].read(), await files[1].read()

    transfer_result = transfer(sess, graph, image_bytes, ref_bytes)
    product = TransferImage(result=[transfer_result, transfer_result])

    return product
