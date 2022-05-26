import io
import cv2
import requests
import base64 # ASCII string -> bytes
import streamlit as st
import tensorflow as tf
from PIL import Image

from utils import transform_image
import streamlit as st
import webbrowser

# SETTING PAGE CONFIG TO WIDE MODE
# st.set_page_config(layout="wide")

def main():
    st.title("BeautyGAN Prototype")
    st.write("")
    st.write("")
    st.warning("정면 사진을 넣어주세요.")
    ref_response = requests.post("http://localhost:8008/beauty/ref", actor="강동원")
    ref_img = ref_response.json()["result"]
    bytes_list = list(map(lambda x: base64.b64decode(x), ref_img))
    st.image(ref_img)
    col1, col2, col3 = st.columns(3)

    # TODO: File Uploader 구현
    with col1:
        uploaded_file = st.file_uploader("Choose no_makeup image", type=["jpg", "jpeg", "png"])
    with col2:
        uploaded_file2 = st.file_uploader("Choose makeup image", type=["jpg", "jpeg", "png"])

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    if uploaded_file and uploaded_file2:
        # TODO: 이미지 View
        image_bytes = uploaded_file.getvalue() # binary 형식
        ref_bytes = uploaded_file2.getvalue() # binary 형식

        no_makeup, makeup = transform_image(image_bytes, ref_bytes)
        files = [('files',(uploaded_file.name, image_bytes, uploaded_file.type)),
                ('files', (uploaded_file2.name, ref_bytes, uploaded_file2.type))]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("No Makeup")
            st.image(no_makeup)

        with col2:
            st.subheader("Makeup")
            st.image(makeup)
         
        with col3:
            # BeautyGAN load
            st.subheader("Result!!!")

            with st.spinner("Inference...."):
                response = requests.post("http://localhost:8008/beauty", files=files)
                output_img = response.json()["result"]
            
                # st.write(type(output_img))
                # st.write(output_img)
                # ASCII코드로 변환된 bytes 데이터(str) -> bytes로 변환 -> 이미지로 디코딩
                bytes_list = list(map(lambda x: base64.b64decode(x), output_img))
                image_list = list(map(lambda x: Image.open(io.BytesIO(x)), bytes_list))

                st.image(image_list[0], caption="Result!!!")
                st.success('Done!')

main()