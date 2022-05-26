from fastapi import FastAPI
from .storage import create_new_bucket, upload_to_bucket, download_from_bucket
# add router
from .routers import classification, beautygan
import re
app = FastAPI()
app.include_router(classification.router)
app.include_router(beautygan.router)

@app.get("/")
def hello_world():
    # bucket 이름
    
    main_bucket = 'bitcoin_storage'
    # 공유된 저장소 이름, upload될 파일명/경로, 로컬파일 경로
    # utb = upload_to_bucket(main_bucket, 'model/11.jpg', 'model/11.jpg')

    # 공유된 저장소 이름, supload할 파일이름/경로, 로컬에 저장할 파일명/경로
    dfb = download_from_bucket(main_bucket, 'models/model.meta', 'models/model2.meta')
    # cnb = create_new_bucket(main_bucket+'2', 'model/11.jpg', 'model/11.jpg')
    return {
        "hello": "world", 
        # "다운로드 됨" : dfb,
        # "업로드 됨" : utb,
        # "새 버킷 만듬" : cnb,
        }
    # return {" Back : FastAPI & Front : Streamlit"}



