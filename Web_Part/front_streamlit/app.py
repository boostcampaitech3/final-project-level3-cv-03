# from distutils.fancy_getopt import fancy_getopt
import io
import time
from turtle import onclick
import requests
import base64 # ASCII string -> bytes
from logger import logger
import streamlit as st
from PIL import Image
import webbrowser

from utils import convert_bytes_to_image
# import webbrowser, json

from front_streamlit import external_components as ec

#%% Custom functions
def uploaded_file_change_callback():
    for k in ['classification_done', 'apply_beautyGAN', 'user_face_confirm', 'router']:
        st.session_state[k] = False

def add_height(n: int=1):
    for i in range(n):
        st.write("")

def new_file():
    st.session_state.refresh = False


#%% Main function
def main():
    global uploaded_file
    # Get css
    with open('./front_streamlit/bootstrap.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Apply custom streamlit button style
    ec.apply_custom_button_style()

    # Navigation bar and page title
    st.markdown(ec.template_navbar(), unsafe_allow_html=True)
    st.markdown(ec.template_cover_heading('Look-Alike Actor'), unsafe_allow_html=True)

    def reset(session_state):
        for key in session_state:
            session_state[key] = False

        session_state['num_face'] = -1
        session_state['refresh'] = True
        return session_state
    
    # Initialize session state key for logic
    def init_session_state():
        session_keys = [
            'refresh',
            'uploaded_file',
            'detected', ## 사용자 이미지에서 얼굴이 탐지 되었는지
            'num_face', ## 얼굴 개수
            'detect_result', ## detect 결과
            'find_actor_clicked',
            'apply_beautyGAN', 
            'classification_done', 
            'classification_img',
            'beautyGAN_img_list',
            'sim_actor_nm'
            'sim_percent',
            'cls_start_time',
            'beauty_start_time',
            'router',
            'files',
            'image_list_1'
            ]

        for session_key in session_keys:
            if session_key not in st.session_state:
                st.session_state[session_key] = False
            st.session_state['num_face'] = -1
    
    init_session_state()

    # Show input guideline message
    if not st.session_state['router']:
        _, main_col2, _ = st.columns(3)
        with main_col2:
            add_height(5)
            input_guide = st.empty()
            input_guide.markdown(ec.bootstrap_warning("※ 아래에 정면 사진을 올려주세요 ※"), unsafe_allow_html=True)
            holder = st.empty()
            uploaded_file = holder.file_uploader("", type=["jpg", "jpeg", "png"], on_change=new_file)        
        
        # Set columns to show uploaded image and classification result image
        _, col2, col3, _ = st.columns(4)
        _, sub_col2, sub_col3, sub_col4, _ = st.columns([2, 2, 1, 1, 2])

        # If get user image
        if uploaded_file and not st.session_state.refresh:
            st.session_state.files = uploaded_file
            st.session_state.uploaded_file = True
            image_bytes = uploaded_file.getvalue()
            files = [
                ('files',(uploaded_file.name, image_bytes, uploaded_file.type))
                ]
            
            if not st.session_state.detected: ## detect를 수행했는지 (중복수행 방지)
                st.session_state.detect_result = requests.post("http://localhost:8008/actorclass/detect", files=files)
                # Detect faces in the uploaded file
                st.session_state.num_face = st.session_state.detect_result.json()["num_box"]
                st.session_state.detected = True
                logger.info(f"Number of Faces : {st.session_state.num_face}")
            
            # Number of face check branch
            if st.session_state.detected and st.session_state.num_face == 0:
                with main_col2:
                    st.error('''죄송합니다. 사진에서 얼굴을 찾을 수 없습니다. 다른 이미지를 업로드해 주세요''')
                    st.session_state.detected = False
                    st.session_state.num_face = -1
            elif st.session_state.detected:
                # Show user uploaded image
                cropped_img = st.session_state.detect_result.json()["result"]
                # ASCII코드로 변환된 bytes 데이터(str) -> bytes로 변환 -> 이미지로 디코딩
                bytes_list_1 = list(map(lambda x: base64.b64decode(x), cropped_img))
                image_list_1 = list(map(lambda x: Image.open(io.BytesIO(x)), bytes_list_1))
                st.session_state.image_list_1 = image_list_1
                if st.session_state.uploaded_file:
                    with col2:
                        st.markdown(ec.template_subheading('업로드한 이미지', 'black', '#AED6F1', 1.5), unsafe_allow_html=True)
                        user_img_field = st.empty()
                        user_img_field.image(uploaded_file, use_column_width=True)
                        holder.empty()
                        input_guide.empty()
                with sub_col2:
                    find_actor_btn = st.button('닮은 배우 찾기')
                    if find_actor_btn:
                        st.session_state.find_actor_clicked = True
                        

            # Get similar actor result and beautyGAN result
            if st.session_state.find_actor_clicked:
                with col3:
                    if not st.session_state.classification_done:
                        with st.spinner('당신과 닮은 배우를 찾는 중 입니다...'):
                            st.session_state.cls_start_time = time.time() # inference
                            cropped_to_bytes = base64.b64decode(cropped_img[0])
                            classfication_files =  [
                                ('files',(uploaded_file.name, cropped_to_bytes, uploaded_file.type))
                            ]
                            response_actor = requests.post("http://localhost:8008/actorclass", files=classfication_files)
                            logger.info(f"Classification Inference Total Time : {time.time() - st.session_state.cls_start_time:.5f}")
                            st.session_state.sim_percent = response_actor.json()['percentage']
                            st.session_state.sim_actor_nm = response_actor.json()['name']
                            logger.info(f"Actor : {st.session_state.sim_actor_nm} | Percent : {st.session_state.sim_percent :.3f}")
                            st.session_state.classification_img = convert_bytes_to_image(response_actor.json()['ref_actor'])
                            # beautyGAN에 보내줄 refer image 추가
                            actor_to_bytes = base64.b64decode(response_actor.json()['ref_actor'])
                            files.append(('files',(uploaded_file.name, actor_to_bytes, uploaded_file.type)))
                            
                            st.session_state.classification_done = True
                            

                            # TODO: Get beautyGAN result
                            st.session_state.beauty_start_time = time.time()
                            response = requests.post("http://localhost:8008/beauty", files=files)
                            output_img = response.json()["result"]
                            logger.info(f"BeautyGAN Inference Total Time : {time.time() - st.session_state.beauty_start_time:.5f}")

                            # ASCII코드로 변환된 bytes 데이터(str) -> bytes로 변환 -> 이미지로 디코딩
                            bytes_list = list(map(lambda x: base64.b64decode(x), output_img))
                            image_list = list(map(lambda x: Image.open(io.BytesIO(x)), bytes_list))

                            # Put beautyGAN result into the session state
                            st.session_state.beautyGAN_img_list = image_list

                            # Show similar actor image
                            st.markdown(ec.template_subheading(
                                f'{st.session_state.sim_actor_nm}님과 {st.session_state.sim_percent*100:.1f}% 유사합니다!',
                                'black', '#D5DBDB', 1.5),
                                    unsafe_allow_html=True)
                            st.image(st.session_state.classification_img, use_column_width=True)
                            logger.info(f"Total Inference Time : {time.time() - st.session_state.cls_start_time}")
                            with sub_col3:
                                refresh_btn = st.button('처음부터 다시하기')
                                if refresh_btn:
                                    st.session_state = reset(st.session_state)
                                    st.experimental_rerun()
                            with sub_col4:
                                apply_beautyGAN_btn = st.button('메이크업 해보기')
                                if apply_beautyGAN_btn:
                                    st.session_state.apply_beautyGAN = True
                    else:                        
                        # Show similar actor image
                        st.markdown(ec.template_subheading(
                            f'{st.session_state.sim_actor_nm}님과 {st.session_state.sim_percent*100:.1f}% 유사합니다!',
                            'black', '#D5DBDB', 1.5),
                                                            unsafe_allow_html=True)
                        st.image(st.session_state.classification_img, use_column_width=True)
                        with sub_col3:
                            refresh_btn = st.button('처음부터 다시하기')
                            if refresh_btn:
                                st.session_state = reset(st.session_state)
                                st.session_state.router = False
                                st.experimental_rerun()
                        with sub_col4:
                            apply_beautyGAN_btn = st.button('메이크업 해보기')
                            if apply_beautyGAN_btn:
                                st.session_state.router = True
                                st.session_state.apply_beautyGAN = True
                                st.experimental_rerun()
                                
    elif st.session_state['router']:
        st.write(st.session_state['apply_beautyGAN'], st.session_state['router'])
        # TODO: 이미지 View
        image_bytes = st.session_state.files.getvalue() # binary 형식
        ref_bytes = st.session_state.classification_img 

        st.write("")
        st.write("")
        st.write("")
        st.write("")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col2:
            st.image(st.session_state.image_list_1[0], use_column_width=True) ############
            st.markdown(ec.template_subheading('당신의 얼굴', 'white', '', 1.2), unsafe_allow_html=True)
        with col3:
            st.image(st.session_state.beautyGAN_img_list[0], use_column_width=True)
            st.markdown(ec.template_subheading('배우 메이크업 적용', 'white', '', 1.2), unsafe_allow_html=True)
        with col4:
            st.image(st.session_state.beautyGAN_img_list[1], use_column_width=True)
            st.markdown(ec.template_subheading('배우의 얼굴', 'white', '', 1.2), unsafe_allow_html=True)
    else:
        init_session_state()

                    

#%% Main part
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(
    page_title='배우고 싶니?', 
    layout="wide",
    )

if __name__=='__main__':
    main()

