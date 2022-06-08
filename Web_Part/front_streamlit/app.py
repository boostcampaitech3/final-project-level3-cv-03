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
import streamlit.components.v1 as components
from frontend import component_zero

#%% Custom functions
def uploaded_file_change_callback():
    for k in ['classification_done', 'apply_beautyGAN', 'user_face_confirm', 'router']:
        st.session_state[k] = False

def add_height(n: int=1):
    for i in range(n):
        st.write("")

def new_file():
    st.session_state.refresh = False

def find_actor_btn_callback():
    st.session_state.find_actor_clicked = True

def run_component(props):
    value = component_zero(key='zero', **props)
    return value

def handle_event(value):
    st.header('Streamlit')
    st.write('Received from component: ', value)      

#%% Main function
def main():
    
    global uploaded_file
    # Get css
    with open('./front_streamlit/bootstrap.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
    with open('./front_streamlit/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Apply backgroung image
    ec.set_bg_hack_url()


    # load script
    
    
    # Navigation bar and page title
    # st.markdown(ec.template_navbar(), unsafe_allow_html=True)
    st.markdown(ec.template_cover_heading('LIKE A STAR'), unsafe_allow_html=True)

    a, b, c, d = st.columns([6, 1, 1, 6])
    with b:
        markdown_string = "[![카카오톡 로고]("
        icon_url = "https://img.shields.io/badge/Kakao-yellow?style=flat-square&logo=KakaoTalk&logoColor=white"
        connect = ")]("
        share_link = "https://sharer.kakao.com/talk/friends/picker/easylink?app_key=228dd3487cef9cea56763dc2d68219c5&ka=sdk%2F1.42.0%20os%2Fjavascript%20sdk_type%2Fjavascript%20lang%2Fen-US%20device%2FWin32%20origin%2Fhttp%253A%252F%252F49.50.164.49%253A30001&validation_action=default&validation_params=%7B%22link_ver%22%3A%224.0%22%2C%22template_object%22%3A%7B%22object_type%22%3A%22feed%22%2C%22content%22%3A%7B%22title%22%3A%22%EB%B0%B0%EC%9A%B0(%EB%90%98)%EA%B3%A0%20%EC%8B%B6%EB%8B%88%3F%22%2C%22description%22%3A%22%EC%B4%88%ED%8A%B9%EA%B8%89%20%EC%9A%B8%ED%8A%B8%EB%9D%BC%20%ED%95%98%EC%9D%B4%ED%8D%BC%20AI%EB%A5%BC%20%EC%82%AC%EC%9A%A9%ED%95%9C%20%EB%8B%AE%EC%9D%80%20%EB%B0%B0%EC%9A%B0%20%EC%B0%BE%EA%B8%B0!%20%EC%95%88%20%ED%95%B4%EB%B3%B4%EA%B3%A0%EB%8A%94%20%EB%AA%BB%20%EB%B0%B0%EA%B8%B8%EA%B1%B8%3F%22%2C%22image_url%22%3A%22https%3A%2F%2Fstorage.googleapis.com%2Fbitcoin_images_storage%2Fshare_thumbnail_image_3.png%22%2C%22link%22%3A%7B%22mobile_web_url%22%3A%22http%3A%2F%2Fwww.simactor.site%3A30001%2F%22%2C%22web_url%22%3A%22http%3A%2F%2Fwww.simactor.site%3A30001%2F%22%7D%7D%2C%22buttons%22%3A%5B%7B%22title%22%3A%22%F0%9F%98%89%EC%B2%B4%ED%97%98%ED%95%B4%EB%B3%B4%EA%B8%B0%22%2C%22link%22%3A%7B%22mobile_web_url%22%3A%22http%3A%2F%2Fwww.simactor.site%3A30001%2F%22%2C%22web_url%22%3A%22http%3A%2F%2Fwww.simactor.site%3A30001%2F%22%7D%7D%5D%7D%7D"
        end = ")"
        st.markdown(markdown_string + icon_url + connect + share_link + end)
    with c:
        markdown_string = "[![깃허브 로고]("
        icon_url = "https://img.shields.io/badge/Github-black?style=flat-square&logo=Github&logoColor=white"
        connect = ")]("
        share_link = "https://github.com/boostcampaitech3/final-project-level3-cv-03"
        end = ")"
        st.markdown(markdown_string + icon_url + connect + share_link + end)
    

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
            'incorrect_beautyGAN', ## 이미지가 beautyGAN에 적절한지
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
            'image_list_1',
            'sim_actor_url'
            ]

        for session_key in session_keys:
            if session_key not in st.session_state:
                st.session_state[session_key] = False
            st.session_state['num_face'] = -1
    
    init_session_state()

    # Show input guideline message
    if not st.session_state['router']:
        
        _, sub_main_col, _ = st.columns([5, 2, 5])
        _, main_col2, _ = st.columns([3, 6, 3])
        with main_col2:
            input_guide = st.empty()
            input_guide.markdown(ec.bootstrap_intro(["AI 메이크업 아티스트가","60여 편의 드라마 작품에서","가장 닮은 배우를 찾은 뒤","메이크업까지 무료로 해드립니다!"]), unsafe_allow_html=True)
            holder = st.empty()
            uploaded_file = holder.file_uploader("", type=["jpg", "jpeg", "png"], on_change=new_file)    
        with sub_main_col:
            add_height(5)
            smp_img_panel = st.empty()
            # smp_img_panel.image('https://storage.googleapis.com/bitcoin_images_storage/thumbnail.jpg', 
            #                     use_column_width='auto')
        
        # Set columns to show uploaded image and classification result image
        _, col2, col3, _ = st.columns(4)
        _, sub_col2, sub_col3, _ = st.columns(4)


        # If get user image
        if uploaded_file and not st.session_state.refresh:
            st.session_state.files = uploaded_file
            st.session_state.uploaded_file = True
            image_bytes = uploaded_file.getvalue()
            image = Image.open(io.BytesIO(image_bytes))
            image_exif = image.getexif()
            if image_exif:
                exif = dict(image_exif.items())
                if exif.get(274) == 1:
                    pass
                else:   
                    if exif.get(274) == 3:
                        image = image.rotate(180, expand=True)
                    elif exif.get(274) == 6:
                        image = image.rotate(270, expand=True)
                    elif exif.get(274) == 8:
                        image = image.rotate(90, expand=True)
                    imgByteArr = io.BytesIO() # <class '_io.BytesIO'>
                    image.save(imgByteArr, format="jpeg") # PIL 이미지를 binary형태의 이름으로 저장
                    image_bytes = imgByteArr.getvalue() # <class 'bytes'>
            
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
                    st.error('''죄송합니다. 사진에서 얼굴을 찾을 수 없습니다. \
                        다른 이미지를 업로드해 주세요''')
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
                        st.markdown(ec.template_subheading('업로드한 이미지', 'black', '#AED6F1'), unsafe_allow_html=True)
                        user_img_field = st.empty()
                        user_img_field.image(image, use_column_width=True)
                        holder.empty()
                        input_guide.empty()
                        smp_img_panel.empty()
                with sub_col2:
                    find_actor_btn = st.empty()
                    find_actor_btn.button('닮은 배우 찾기', on_click=find_actor_btn_callback)
                    # if find_actor_btn:
                    #     st.session_state.find_actor_clicked = True
                        

            # Get similar actor result and beautyGAN result
            if st.session_state.find_actor_clicked:
                # Remove fint actor button
                find_actor_btn.empty()
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
                            st.session_state.sim_actor_url = response_actor.json()['url']
                            logger.info(f"Actor : {st.session_state.sim_actor_nm} | Percent : {st.session_state.sim_percent :.3f}")
                            st.session_state.classification_img = convert_bytes_to_image(response_actor.json()['ref_actor'])
                            # beautyGAN에 보내줄 refer image 추가
                            actor_to_bytes = base64.b64decode(response_actor.json()['ref_actor'])
                            files.append(('files',(uploaded_file.name, actor_to_bytes, uploaded_file.type)))
                            
                            st.session_state.classification_done = True
                            

                            # TODO: Get beautyGAN result
                            st.session_state.beauty_start_time = time.time()
                            response = requests.post("http://localhost:8008/beauty", files=files)
                            result_beauty = response.json()["result"]
                            if result_beauty == "Incorrect": ## BeautyGAN 이미지 에러!
                                st.session_state.incorrect_beautyGAN = True
                            else:
                                output_img = result_beauty
                                logger.info(f"BeautyGAN Inference Total Time : {time.time() - st.session_state.beauty_start_time:.5f}")

                                # ASCII코드로 변환된 bytes 데이터(str) -> bytes로 변환 -> 이미지로 디코딩
                                bytes_list = list(map(lambda x: base64.b64decode(x), output_img))
                                image_list = list(map(lambda x: Image.open(io.BytesIO(x)), bytes_list))

                                # Put beautyGAN result into the session state
                                st.session_state.beautyGAN_img_list = image_list

                            # Show similar actor image
                            st.markdown(ec.template_subheading(
                                f'{st.session_state.sim_actor_nm}님과 {st.session_state.sim_percent*100:.1f}% 유사합니다!',
                                'black', '#D5DBDB'),
                                    unsafe_allow_html=True)
                            st.image(st.session_state.classification_img, use_column_width=True)
                            logger.info(f"Total Inference Time : {time.time() - st.session_state.cls_start_time}")
                            with sub_col2:
                                refresh_btn = st.button('처음부터 다시하기')
                                if refresh_btn:
                                    st.session_state = reset(st.session_state)
                                    st.experimental_rerun()
                            with sub_col3:
                                apply_beautyGAN_btn = st.button('메이크업 해보기')
                                if apply_beautyGAN_btn:
                                    st.session_state.apply_beautyGAN = True
                    else:                        
                        # Show similar actor image
                        st.markdown(ec.template_subheading(
                            f'{st.session_state.sim_actor_nm}님과 {st.session_state.sim_percent*100:.1f}% 유사합니다!',
                            'black', '#D5DBDB'),
                                                            unsafe_allow_html=True)
                        st.image(st.session_state.classification_img, use_column_width=True)
                        logger.info(f"Total Inference Time : {time.time() - st.session_state.cls_start_time}")
                        with sub_col2:
                            refresh_btn = st.button('처음부터 다시하기')
                            if refresh_btn:
                                st.session_state = reset(st.session_state)
                                st.session_state.router = False
                                st.experimental_rerun()
                        with sub_col3:
                            apply_beautyGAN_btn = st.button('메이크업 해보기')
                            if apply_beautyGAN_btn:
                                st.session_state.router = True
                                st.session_state.apply_beautyGAN = True
                                st.experimental_rerun()
                                
    elif st.session_state['router']:
        ## BeautyGAN 이미지를 인식하지 못하는 경우!
        if st.session_state.incorrect_beautyGAN:
                st.error("저희의 AI 메이크업 아티스트가 얼굴을 제대로 인식하지 못했습니다. \
                    눈, 코, 입이 잘 보이도록 사진을 찍어주세요!")
        # TODO: 이미지 View
        image_bytes = st.session_state.files.getvalue() # binary 형식

        # add_height(4)
        st.balloons()
        _, col2, col3, col4, _ = st.columns(5)
        _, beautyGAN_btn_col, test, test2, _  = st.columns([2, 3,3,3, 2])
        with col2:
            st.image(st.session_state.image_list_1[0], use_column_width=True) ############
            st.markdown(ec.photo_subheading('당신의 얼굴', 'white', ''), unsafe_allow_html=True)
        with col3:
            st.image(st.session_state.beautyGAN_img_list[0], use_column_width=True)
            st.markdown(ec.photo_subheading('배우 메이크업 적용', 'white', ''), unsafe_allow_html=True)
        with col4:
            st.image(st.session_state.beautyGAN_img_list[1], use_column_width=True)
            st.markdown(ec.photo_subheading('배우의 얼굴', 'white', ''), unsafe_allow_html=True)
        with beautyGAN_btn_col:
            share_btn = st.button('카카오톡으로 공유하기')
            if share_btn:
                props = {
                    'actor': st.session_state.sim_actor_nm,
                    'percent' : round(st.session_state.sim_percent * 100, 1),
                    'url' : st.session_state.sim_actor_url,
                }
                run_component(props)
            
        with test:
            refresh_btn = st.button('처음부터 다시하기')
            if refresh_btn:
                st.session_state = reset(st.session_state)
                st.session_state.router = False
                st.experimental_rerun()
        with test2:
            link = 'https://docs.google.com/forms/d/e/1FAIpQLSf2yrMEZM6GQiul69EDGQ5OPKK6ELDGFdZfu7cYEcsWelw4eQ/viewform?usp=sf_link'
            st.markdown(ec.footer_button(link), unsafe_allow_html=True)
    else:
        init_session_state()
    
    st.markdown(ec.footer(), unsafe_allow_html=True)
                    

#%% Main part
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(
    page_title='배우고 싶니?', 
    layout="wide",
    page_icon="/opt/ml/final_project/Web_Part/front_streamlit/imgs/bitcoinpizza.png"
    )



if __name__=='__main__':
    main()
    
