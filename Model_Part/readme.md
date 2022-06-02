## Getting Started

1. Python requirements
    
    `Python`: 3.7.13
    
2. Installation
    1. 가상 환경을 설정합니다
    2. 프로젝트의 의존성을 설치합니다
        
        `requirements_models.txt`를 사용하여 라이브러리를 설치합니다.
        
        ```
        > pip install -r requirements_models.txt
        
        ```
        
3. Image download
`cleaned_v1.tar`를 다운로드하고 압축을 해제합니다.
    
    ```bash
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AZv__u19VWZLKxcW6IfgJ0tU9GS7urrD' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AZv__u19VWZLKxcW6IfgJ0tU9GS7urrD" -O cleaned_v1.tar && rm -rf /tmp/cookies.txt && tar -xvf cleaned_v1.tar
    ```
    
4. Image cropping
    
    `image_cropper_insight.py`를 실행합니다.
    
    - 최소 얼굴 사이즈 기준으로 박스가 하나 존재하는 경우에만 images 폴더에 저장됩니다.
        
        0개면 noface, 2개 이상이면 manyface 폴더에 저장됩니다.
        
    - **Crop 되는** **이미지 사이즈, 최소 얼굴 사이즈, Det_size를 변경하실 수 있습니다.**
    
    ```bash
    python image_cropper_insight.py
    ```
    
    ****❗중간에 서버가 멈추어 연결이 끊기는 현상이 발생할 수 있습니다!****
    
        10분 정도 지나면 다시 연결이 가능하고, 
    
        코드 내부의 count 변수를 변경하여 원하는 iter부터 다시 진행하시면 됩니다
    
5. 데이터셋 나누기
    
    `to_csv.py`를 실행시켜 데이터를 train, valid로 나눕니다
    
    ```bash
    python to_csv.py
    ```
    
6. `Base_classification.ipynb` 에서 실험을 진행합니다!