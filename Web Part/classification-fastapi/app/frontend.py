import io
from model import load_model
import streamlit as st
import requests

from PIL import Image

##### train 한대로 리스트를 정의해주세요. (필수) #####
celeb_list = [
        '공유', '권나라', '문채원', '박하선', '배두나', '신민아', '신성록', '안재현', '여진구', '유아인',
        '이다희', '이병헌', '이선균', '이시영', '전미도', '정은지', '조정석', '차승원', '한선화', '현빈',
    ]

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")


def main():
    st.title("배우고 싶니?!?!")
    st.header("닮은 꼴 연예인 찾기 ")

    # File Uploader
    uploaded_file = st.file_uploader("본인의 사진을 업로드", type=['jpg', 'jpeg', 'png', 'heic'])

    if uploaded_file:
        # 이미지 View
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption="Uploaded Image")
        # 예측
        st.write("닮은 꼴 배우를 찾는 중...")
        
        files = [
            ('files', (
                uploaded_file.name,
                image_bytes,
                uploaded_file.type,
            ))
        ]
        response = requests.post("http://localhost:8001/order", files=files)
        
        label = response.json()['products'][0]['result']
        st.write(f"닮은 배우는 {celeb_list[label]}입니다!")


main()