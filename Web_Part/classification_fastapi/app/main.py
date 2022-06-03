from datetime import datetime
from uuid import UUID, uuid4
from fastapi import FastAPI, UploadFile, File
from fastapi.param_functions import Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Union

from datetime import datetime

from app.model import efficientnet, load_model, get_prediction

app = FastAPI()

##### 훈련시킨 배우들 수 (필수) #####
celeb_num = 20


class Product(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: int

class Order(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    products: List[Product] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


orders = [] # 임시로 In Memory

@app.get("/order", description="주문 리스트 가져오기")
def get_orders() -> List[Order]:
    return orders


@app.get("/order/{order_id}", description="Order 정보를 가져옵니다")
def get_order(order_id: UUID) -> Union[Order, dict]:
    order = get_order_by_id(order_id=order_id)
    if not order:
        return {"message": "주문 정보를 찾을 수 없습니다."}
    return order


def get_order_by_id(order_id: UUID) -> Optional[Order]:
    return next((order for order in orders if order.id == order_id), None)


class InferenceImageProduct(Product):
    name: str = "Inference_Image"
    result: Optional[int]


@app.post("/order", description="주문을 요청합니다.")
async def make_order(
        # celeb_num: int,
        files: List[UploadFile] = File(...),):
    model = load_model(celeb_num=celeb_num)
    model.eval()

    products = []
    for file in files:
        image_bytes = await file.read()
        inference_result = get_prediction(model=model, image_bytes=image_bytes)
        product = InferenceImageProduct(result=inference_result)
        products.append(product)
    
    new_order = Order(products=products)
    orders.append(new_order)
    return new_order
