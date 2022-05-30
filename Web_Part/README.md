# 배우고 싶니?
Streamlit + FastAPI를 이용한 닮은꼴 화장 모델 온라인 서빙 


## Directory 구조
   ```shell
   Web_Part
   ├── back_fastapi
   │   └── app
   │       ├── __main__.py
   │       ├── main.py ---> fastapi 실행 스크립트
   │       ├── routers
   │       │   ├── face_classifier.py ---> classifier 라우터
   │       │   └── face_makeup.py ---> beautygan 라우터
   │       ├── storage.py ---> storage 관련 함수 정의 
   │       └── utils.py
   ├── front_streamlit
   │   ├── app.py ---> steamlit 실행 스크립트
   │   ├── bootstrap.css
   │   └── utils.py
   ├── models
   │   ├── beautygan
   │   │   ├── beautygan_model.py ---> beautygan 모델 관련 함수 정의(eg. model_load 등)
   │   │   └── weights
   │   └── efficientnet
   │       ├── efficientnet_model.py ---> classification 모델 관련 함수 정의(eg. model_load 등)
   │       └── weights
   ├── Makefile ---> streamlit & beautygan 동시 실행을 위한 파일
   ├── README.md
   ├── actor.json ---> classification gt & data url
   └── requirements_web.txt
   ```
## Getting Started
0. Python requirements  
   `Python`: 3.7.13  

1. Installation
   1. 가상 환경을 설정합니다
     
   2. 프로젝트의 의존성을 설치합니다

      1. `requirements_web.txt`를 사용하여 라이브러리를 설치합니다.    
         ```shell
         > pip install -r requirements_web.txt 
         ```
      2. `conda`를 사용하여 `dlib` 라이브러리를 추가로 설치합니다.
         ```shell
         conda install -c conda-forge dlib
         ```
      
   3. 아래 url에 들어가서 beautygan의 가중치는 Web_Part/models/beautygan/weights 폴더 안으로, efficientnet의 가중치는 Web_Part/models/efficientnet/weights 다운받습니다.  
      https://drive.google.com/drive/folders/1pgVqnF2-rnOxcUQ3SO4JwHUFTdiSe5t9

   4. ```shell
      > cd Web_Part
      ``` 

   5. Frontend(Streamlit)와 Server(FastAPI)를 같이 실행합니다
      ```shell
      > make -j 2 run_app
      ```