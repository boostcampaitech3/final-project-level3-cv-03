![Logo.jpg](https://user-images.githubusercontent.com/37561451/173091343-45a49d7f-4620-43a4-b504-ead506e0934d.png)

## 1️⃣ Introduction

### 1) Background

​		기존의 닮은 배우(or 연예인) 찾기 서비스가 실제 사용자와 크게 닮지 않다는 점에서 착안

### 2) Project Objective

- 사용자가 배우와 닮았다고 느낄 수 있도록 개선한 서비스를 웹으로 제공
- Efficientnet과 BeautyGAN을 사용하여 최소한의 서비스를 구현

![Untitled](https://user-images.githubusercontent.com/37561451/173113075-d798d36e-949e-49e7-9ce8-9b0c29d0ccb8.png)

------

## 2️⃣ Demo 영상

<img src="https://user-images.githubusercontent.com/37561451/173114020-0ebc9e4c-41b4-4b5c-b2bb-3b0c65efba2f.gif" width="55%" />

------

## 3️⃣ Service Architecture

### 1) Directory 구조

```shell
   final-project-level3-cv-03
   ├── 📁 Crawiling_Part⋮
   │    └──  ⋮
   ├── 📁 Model_Part
   │    └──  ⋮
   ├── 📁 Tools
   │    └──  ⋮
   ├── 📁 Web_Part
   │    ├── 📁 back_fastapi
   │    │   └── 📁 app
   │    │       ├── 💾 __main__.py
   │    │       ├── 💾 main.py
   │    │       ├── 📁 routers
   │    │       │   ├── 💾 face_classifier.py
   │    │       │   └── 💾 face_makeup.py
   │    │       ├── 💾 storage.py
   │    │       └── 💾 utils.py
   │    ├── 📁 front_streamlit
   │    │   ├── 💾 app.py
   │    │   ├── 💾 utils.py
   │    │   └──  ⋮ 
   │    ├── 📁 kakaotalk_share
   │    │    ├── 💾 __init__.py
   │    │    └── 💾 index.html
   │    ├── 📁 log
   │    │    └── ⋮ 
   │    ├── 📁 models
   │    │   ├── 📁 beautygan
   │    │   │   ├── 💾 beautygan_model.py
   │    │   │   └── 📁 weights
   │    │   └── 📁 efficientnet
   │    │       ├── 💾 efficientnet_model.py
   │    │       └── 📁 weights
   │    ├── 💾 actor.json
   │    ├── 💾 config.yaml
   │    ├── 💾 logger.py
   │    └── 💾 Makefile 
   └── 💾 requirements.txt

```

------

## 4️⃣ DataSet

### 1) 데이터셋 구성 파이프라인

![dataflow](https://user-images.githubusercontent.com/37561451/173118470-c75e7061-62f1-49b4-96a5-4af453f5facd.png)

### 2) 데이터셋 수집

- **총** **51221**장 → 배우 별 **8:2**의 비율로 **train set**과 **valid set**구성
- **mtcnn**을 이용해 얼굴이 하나만 탐지된 사진 중 일정한 화질 이상의 이미지를 수집 
- **배우 이름, 시사회, 화보**등 키워드를 검색에 이용, **배우 당 500개**의 이미지를 크롤링

------

## 5️⃣ Modeling

### 1) Flow Chart

![flowchart](https://user-images.githubusercontent.com/37561451/173102952-68b35df9-1119-45ef-bbe4-42131544915f.png)

### 2) Preprocessing

- 선글라스 착용, 2개 이상의 얼굴, 옆모습 제외
- JPEG 형식 통일
- Insight face를 사용
  - 다수의 얼굴이 detect 되는 경우 제외
  - 얼굴 부분이 너무 작거나 없는 경우 제외
- algin, crop

------

## 6️⃣ Product Serving

### 1) FrontEnd (Streamlit)

- 사용자가 이미지를 업로드할 인터페이스
- 닮은 배우 이미지, 일치율, 배우 이름 출력
- 카카오톡 공유 버튼
- 각종 UI 디자인
- 도메인 주소 할당

### 2) BackEnd (FastAPI)

   ![flow chart](https://user-images.githubusercontent.com/78528903/173296222-258e2bef-e0a9-4c16-ad0d-fee829871e1a.png)
- 1.user가 이미지 업로드 → 2. server에 detect 요청 → 전처리 → 3. client에 결과 반환 → 4. client는 얼굴이 감지된 경우와 감지되지 않은 경우를 분기처리 → 5. server는 classification 수행 시 닮은 배우 이름을 통해 GCP storage에서 배우 이미지를 가져와 client로 보냄   

<br/>

   ![image](https://user-images.githubusercontent.com/78528903/173296349-4e5f2a4d-88e8-4a51-aba5-a82523c23657.png)
- 1.client에서 user이미지, 배우 이미지와 함께 server에 makeup요청 → 2. server가 전처리 후 makeup transfer 수행 → 3. 배우의 화장이 입혀진 user 이미지를 client로 보냄

### 3) Logging
- Google Cloud Bigquery를 사용하여 로깅 구축
- 수집 데이터 목록
   1. user와 닮은 배우의 이름
   2. user와 배우와의 일치율
   3. backend에서 BeautyGAN inference시간
   4. frontend에서 makeup-transfer request-response 시간
   5. 사용자가 image로 결과를 보기까지의 시간
   6. 전처리 과정에서 user 사진에서 detect된 얼굴의 수
   7. backend에서 classification inference시간
   8. frontend에서 classification request-response 시간

### 4) Github Action

- github action을 통해 간단한 배포 자동화 구축
- github main으로 push event 발생 시 google compute engine에 배포를 요청

### 5) Getting Started!

1. Python requirements
   `Python`: 3.7.13

2. Installation

   1. 가상 환경을 설정합니다

   2. 프로젝트의 의존성을 설치합니다

      - ```
        requirements.txt
        ```

        를 사용하여 라이브러리를 설치합니다.

        ```
        > pip install -r requirements.txt 
        ```

   3. 아래 url에 들어가서 beautygan의 가중치는 Web_Part/models/beautygan/weights 폴더 안으로, efficientnet의 가중치는 Web_Part/models/efficientnet/weights 다운받습니다.

      - beautygan 가중치 : <https://drive.google.com/drive/folders/1pgVqnF2-rnOxcUQ3SO4JwHUFTdiSe5t9>
      - efficientnet 가중치 : <https://drive.google.com/drive/folders/113pJ2YZa_AuOGWpan7qotU3s374KzpbC?usp=sharing>

   4. ```
      > cd Web_Part
      ```

   5. Frontend(Streamlit)와 Server(FastAPI)를 같이 실행합니다

      ```
      > make -j 2 run_app
      ```



------

## 7️⃣  Appendix

### 타임라인

![timeline](https://user-images.githubusercontent.com/37561451/173107042-984b7194-a7c6-43c1-a642-a70067f76e6b.png)

### 협업 Tools

- **notion**

  - notion을 활용해 **1차 기능 구현 계획**을 세우고 각 part별로 업무를 작성
  - **project kanban board**를 통해 **업무, part, 진행률, 담당자**를 명시하여 서로의 작업 상황을 공유
  - [bittcoin notion link](https://sand-bobolink-9c4.notion.site/Final-Project-0e0a8f40e20143c89e06439e6af43b9a)

  

- **github**

  - 전체적으로 **github flow**를 사용하여 repo 관리
  - **release branch**를 통해 2.0.1까지 총 4가지 버전 배포

------

## 8️⃣ 팀원 소개
![image](https://user-images.githubusercontent.com/78528903/173313460-444b8f29-f743-422f-9586-d7356c51ed61.png)

