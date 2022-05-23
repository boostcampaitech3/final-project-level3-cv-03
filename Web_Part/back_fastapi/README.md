# FastAPI
FastAPI을 이용한 모델 온라인 서빙 

## Getting Started
0. Python requirements  
   `Python`: 3.7  
1. Installation
   1. 가상 환경을 설정합니다
     
   2. 프로젝트의 의존성을 설치합니다
        ```shell
        > pip install -r requirements.txt 
        ```
   3. 아래 url에 들어가서 beautygan의 가중치를 models 폴더 안으로 다운받습니다.  
      https://drive.google.com/drive/folders/1pgVqnF2-rnOxcUQ3SO4JwHUFTdiSe5t9

   3. 애플리케이션을 실행합니다
      ```shell
      > python -m app
      ```  
   4. Frontend(Streamlit)와 Server를 같이 실행합니다
      ```shell
      make -j 2 run_app
      ```

