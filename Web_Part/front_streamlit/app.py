from distutils.fancy_getopt import fancy_getopt
import io
import cv2
import requests
import base64 # ASCII string -> bytes
import streamlit as st
import tensorflow as tf
from PIL import Image

from utils import transform_image, convert_bytes_to_image
import webbrowser, json

import front_streamlit.external_components as ec

def uploaded_file_change_callback():
    for k in ['classification_done', 'apply_beautyGAN', 'user_face_confirm']:
        st.session_state[k] = False
    
#%% Main function
def main():
    # Get css
    with open('./front_streamlit/bootstrap.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Apply custom streamlit button style
    ec.apply_custom_button_style()

    # Navigation bar and page title
    st.markdown(ec.template_navbar(), unsafe_allow_html=True)
    st.markdown(ec.template_cover_heading('BeautyGAN Prototype'), unsafe_allow_html=True)

    # Initialize session state key for logic
    session_keys = [
        'user_face_confirm',
        'apply_beautyGAN', 
        'classification_done', 
        'classification_img',
        'beautyGAN_img_list',
        'sim_actor_nm'
        ]
    for session_key in session_keys:
        if session_key not in st.session_state:
            st.session_state[session_key] = False

    # Show input guideline message
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown(ec.bootstrap_warning("정면 사진을 올려주세요."), unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])        

    # Set columns to show uploaded image and classification result image
    _, col2, col3, _ = st.columns(4)

    # If get user image
    if uploaded_file:
        # Show user uploaded image
        image_bytes = uploaded_file.getvalue()
        no_makeup = transform_image(image_bytes)
        files = [
            ('files',(uploaded_file.name, image_bytes, uploaded_file.type))
            ]


        with col2:
            st.markdown(ec.template_subheading('업로드한 이미지', 'black', '#AED6F1'), unsafe_allow_html=True)
            st.image(uploaded_file, use_column_width=True)
            
            face_detected = True

            # Face detection branch (fit for col2)
            if face_detected:
                st.markdown(ec.template_subheading('박스 안쪽에 얼굴이 잘 위치해있나요?', 'black', '#AED6F1', '125%'), unsafe_allow_html=True)
            else:
                st.error('''죄송합니다. 얼굴을 찾을 수 없습니다. 다른 이미지를 업로드해 주세요''')
        
        # Face detection main branch
        if face_detected:
            _, sub_col1, sub_col2, _ = st.columns([2, 1, 1, 4])
            with sub_col1:
                user_face_true_btn = st.button('네')
            with sub_col2:
                user_face_false_btn = st.button('아니오') 

            # If the detected face is found to be inaccurate by the user
            if user_face_false_btn:
                st.session_state.user_face_confirm = False
                st.session_state.apply_beautyGAN = False
                st.session_state.classification_done = False

                _, col2, col3, _ = st.columns(4)
                with col2:
                    st.markdown(ec.template_subheading('죄송합니다. 다른 사진을 업로드해주세요.', 'white', '', '105%'), unsafe_allow_html=True)
            
            # If the detected face is found to be accurate by the user
            if user_face_true_btn:
                st.session_state.user_face_confirm = True

            if st.session_state.user_face_confirm:
                # Get similar actor result and beautyGAN result
                with col3:
                    if not st.session_state.classification_done:
                        with st.spinner('당신과 닮은 배우를 찾는 중 입니다...'):
                            response_actor = requests.post("http://localhost:8008/actorclass", files=files)
                            percentage = response_actor.json()['percentage']
                            st.session_state.sim_actor_nm = response_actor.json()['name']
                            st.session_state.classification_img = convert_bytes_to_image(response_actor.json()['ref_actor'])
                            # beautyGAN에 보내줄 refer image 추가
                            actor_to_bytes = base64.b64decode(response_actor.json()['ref_actor'])
                            files.append(('files',(uploaded_file.name, actor_to_bytes, uploaded_file.type)))
                                                    
                            st.session_state.classification_done = True

                            # TODO: Get beautyGAN result
                            response = requests.post("http://localhost:8008/beauty", files=files)
                            output_img = response.json()["result"]
                        
                            # ASCII코드로 변환된 bytes 데이터(str) -> bytes로 변환 -> 이미지로 디코딩
                            bytes_list = list(map(lambda x: base64.b64decode(x), output_img))
                            image_list = list(map(lambda x: Image.open(io.BytesIO(x)), bytes_list))

                            # Put beautyGAN result into the session state
                            st.session_state.beautyGAN_img_list = image_list

                            # Show similar actor image
                            st.markdown(ec.template_subheading(f'당신과 닮은 배우는 {percentage*100:.2f}%로 {st.session_state.sim_actor_nm}!', 'black', '#D5DBDB'),
                                        unsafe_allow_html=True)
                            st.image(st.session_state.classification_img, use_column_width=True)
                            apply_beautyGAN_btn = st.button('메이크업 따라하기')
                            if apply_beautyGAN_btn:
                                st.session_state.apply_beautyGAN = True
                    else:                        
                        # Show similar actor image
                        st.markdown(ec.template_subheading(f'당신과 닮은 배우는 {st.session_state.sim_actor_nm}!', 'black', '#D5DBDB'),
                                                            unsafe_allow_html=True)
                        st.image(st.session_state.classification_img, use_column_width=True)
                        apply_beautyGAN_btn = st.button('메이크업 따라하기')
                        if apply_beautyGAN_btn:
                            st.session_state.apply_beautyGAN = True

        if st.session_state.user_face_confirm and st.session_state.apply_beautyGAN:
            # TODO: 이미지 View
            image_bytes = uploaded_file.getvalue() # binary 형식
            ref_bytes = st.session_state.classification_img 

            def crop_face(image_raw):
                return image_box

            st.write("")
            # st.write("")

            col1, col2, col3, col4, col5 = st.columns(5)
            with col2:
                st.markdown(ec.template_subheading('당신의 얼굴', 'white', ''), unsafe_allow_html=True)
                st.image(no_makeup, use_column_width=True)
          
            with col3:
                # BeautyGAN load
                st.markdown(ec.template_subheading('배우 메이크업 적용', 'white', ''), unsafe_allow_html=True)
                st.image(st.session_state.beautyGAN_img_list[0], use_column_width=True)

            with col4:
                st.markdown(ec.template_subheading('배우의 얼굴', 'white', ''), unsafe_allow_html=True)
                st.image(st.session_state.beautyGAN_img_list[1], use_column_width=True)


#%% Main part
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(
    page_title='배우고 싶니?', 
    layout="wide",
    )

if __name__=='__main__':
    main()

