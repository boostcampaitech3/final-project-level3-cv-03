from fastapi import FastAPI
from .storage import create_new_bucket, upload_to_bucket, download_from_bucket

# add router
from .routers import face_classifier, face_makeup

app = FastAPI()
app.include_router(face_classifier.router)
app.include_router(face_makeup.router)


@app.get("/")
def hello_world():
    # bucket 이름
    
    images_bucket = 'bitcoin_images_storage'
    models_bucket = 'bitcoin_model_storage'
    
    '''
    # 디렉토리 지정 시 미리 local에 생성되어 있어야 하고 파일명은 다르게 download하셔도 괜찮습니다.

    upload_to_bucket(공유된 저장소 이름, upload될 파일명/경로, 로컬파일 경로)
    create_new_bucket(생성할 bucket 이름, 'model/11.jpg', 'model/11.jpg')
    공유된 저장소 이름, upload할 파일이름/경로, 로컬에 저장할 파일명/경로
    '''
    # files = ['checkpoint', 'model.data-00000-of-00001', 'model.index', 'model.meta']
    # for file in files:
    #     download_from_bucket(models_bucket, f'models/{file}', f'weights/{file}')
    
    # download_from_bucket(models_bucket, f'models/epoch_20.pt', f'weights/epoch_20.pt')
    return {" Back : FastAPI & Front : Streamlit"}
