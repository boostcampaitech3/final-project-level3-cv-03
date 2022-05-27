from distutils.fancy_getopt import fancy_getopt
import io
import cv2
import requests
import base64 # ASCII string -> bytes
import streamlit as st
import tensorflow as tf
from PIL import Image

from utils import transform_image
import webbrowser

#%% Bootstrap components
def bootstrap_block_level_button(text):
    return f"""
    <button type="button" class="btn btn-primary btn-lg btn-block">{text}</button>
    """


def bootstrap_card():
    return f"""
    <div class="card" style="width: 18rem;">
        <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="card-link">Card link</a>
            <a href="#" class="card-link">Another link</a>
        </div>
    </div>
    """


def bootstrap_warning(text: str):
    return f"""
        <div class="alert alert-dark" role="alert", style="margin:3rem; background-color:#FCF3CF; margin-top:18px; font-family:verdana; font-size:150%; text-align:center;">
        {text}
        </div>
    """


def bootstrap_navbar():
    return """
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">배우고싶니</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <a class="nav-item nav-link active" href="#">Home <span class="sr-only">(current)</span></a>
                <a class="nav-item nav-link" href="#">Features</a>
                <a class="nav-item nav-link" href="#">Pricing</a>
                <a class="nav-item nav-link disabled" href="#">Disabled</a>
            </div>
        </div>
    </nav>
    """

def template_navbar():
    return """
    <header class="masthead mb-auto">
        <div class="inner">
          <h3 class="masthead-brand">배우고싶니</h3>
          <nav class="nav nav-masthead justify-content-center">
            <a class="nav-link active" href="#">Home</a>
            <a class="nav-link" href="#">Service Page</a>
            <a class="nav-link" href="#">Contact Us</a>
          </nav>
        </div>
    </header>
    """


def template_cover_heading(head_title):
    return f"""
    <h1 style="text-align:center; color=black; font-weight:bold; font-size:400%">{head_title}</h1>
    """


def template_subheading(text: str, color: str='black', background_color: str=None, font_size: str='200%'):
    return f"""
    <h2 style="text-align:center; color:{color}; background-color:{background_color}; font-size:{font_size}">{text}</h2>
    """


def template_body():
    return """
    <body class="text-center" data-new-gr-c-s-check-loaded="14.1062.0" data-gr-ext-installed="">

        <div class="cover-container d-flex h-100 p-3 mx-auto flex-column">
            <header class="masthead mb-auto">
                <div class="inner">
                <h3 class="masthead-brand">Cover</h3>
                <nav class="nav nav-masthead justify-content-center">
                    <a class="nav-link active" href="#">Home</a>
                    <a class="nav-link" href="#">Features</a>
                    <a class="nav-link" href="#">Contact</a>
                </nav>
                </div>
            </header>

            <main role="main" class="inner cover">
                <h1 class="cover-heading">Cover your page.</h1>
                <p class="lead">Cover is a one-page template for building simple and beautiful home pages. Download, edit the text, and add your own fullscreen background photo to make it your own.</p>
                <p class="lead">
                    <a href="#" class="btn btn-lg btn-secondary">Learn more</a>
                </p>
            </main>

            <footer class="mastfoot mt-auto">
                <div class="inner">
                  <p>Cover template for <a href="https://getbootstrap.com/">Bootstrap</a>, by <a href="https://twitter.com/mdo">@mdo</a>.</p>
                </div>
            </footer>
        </div>


        <!-- Bootstrap core JavaScript
        ================================================== -->
        <!-- Placed at the end of the document so the pages load faster -->
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
    
    </body>
    """


def template_album():
    return """
    <div class="container">
            <div class="row">
            <div class="col-md-4">
                <div class="card mb-4 box-shadow">
                <img class="card-img-top" data-src="holder.js/100px225?theme=thumb&amp;bg=55595c&amp;fg=eceeef&amp;text=Given Image" alt="Given Image [100%x225]" style="height: 225px; width: 100%; display: block;" src="data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22288%22%20height%3D%22225%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20288%20225%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_180ff073af8%20text%20%7B%20fill%3A%23eceeef%3Bfont-weight%3Abold%3Bfont-family%3AArial%2C%20Helvetica%2C%20Open%20Sans%2C%20sans-serif%2C%20monospace%3Bfont-size%3A14pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_180ff073af8%22%3E%3Crect%20width%3D%22288%22%20height%3D%22225%22%20fill%3D%22%2355595c%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%2296.84375%22%20y%3D%22118.8%22%3EGiven Image%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E" data-holder-rendered="true">
                <div class="card-body">
                    <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                    <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                        <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
                        <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
                    </div>
                    <small class="text-muted">9 mins</small>
                    </div>
                </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card mb-4 box-shadow">
                <img class="card-img-top" data-src="holder.js/100px225?theme=thumb&amp;bg=55595c&amp;fg=eceeef&amp;text=Thumbnail" alt="Thumbnail [100%x225]" src="data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22288%22%20height%3D%22225%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20288%20225%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_180ff073af8%20text%20%7B%20fill%3A%23eceeef%3Bfont-weight%3Abold%3Bfont-family%3AArial%2C%20Helvetica%2C%20Open%20Sans%2C%20sans-serif%2C%20monospace%3Bfont-size%3A14pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_180ff073af8%22%3E%3Crect%20width%3D%22288%22%20height%3D%22225%22%20fill%3D%22%2355595c%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%2296.84375%22%20y%3D%22118.8%22%3EMake Up%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E" data-holder-rendered="true" style="height: 225px; width: 100%; display: block;">
                <div class="card-body">
                    <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                    <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                        <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
                        <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
                    </div>
                    <small class="text-muted">9 mins</small>
                    </div>
                </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card mb-4 box-shadow">
                <img class="card-img-top" data-src="holder.js/100px225?theme=thumb&amp;bg=55595c&amp;fg=eceeef&amp;text=Thumbnail" alt="Thumbnail [100%x225]" src="data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22288%22%20height%3D%22225%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20288%20225%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_180ff073af9%20text%20%7B%20fill%3A%23eceeef%3Bfont-weight%3Abold%3Bfont-family%3AArial%2C%20Helvetica%2C%20Open%20Sans%2C%20sans-serif%2C%20monospace%3Bfont-size%3A14pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_180ff073af9%22%3E%3Crect%20width%3D%22288%22%20height%3D%22225%22%20fill%3D%22%2355595c%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%2296.84375%22%20y%3D%22118.8%22%3EResult%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E" data-holder-rendered="true" style="height: 225px; width: 100%; display: block;">
                <div class="card-body">
                    <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                    <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                        <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
                        <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
                    </div>
                    <small class="text-muted">9 mins</small>
                    </div>
                </div>
                </div>
            </div>
            </div>
        </div>
    """

def main():
    # Get css
    with open('./front_streamlit/bootstrap.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


    st.markdown(template_navbar(), unsafe_allow_html=True)
    st.markdown(template_cover_heading('BeautyGAN Prototype'), unsafe_allow_html=True)
    
    # Show warning message
    # st.warning("정면 사진을 넣어주세요.")
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown(bootstrap_warning("정면 사진을 넣어주세요."), unsafe_allow_html=True)

    # ref_response = requests.post("http://localhost:8008/beauty/ref", actor="강동원")
    # ref_img = ref_response.json()["result"]
    # bytes_list = list(map(lambda x: base64.b64decode(x), ref_img))
    # st.image(ref_img)

    col1, col2, col3, col4 = st.columns(4)

    # TODO: File Uploader 구현
    with col2:
        uploaded_file = st.file_uploader("사진을 넣어주세요", type=["jpg", "jpeg", "png"])
    with col3:
        uploaded_file2 = st.file_uploader("Choose makeup image", type=["jpg", "jpeg", "png"])

    # st.markdown(template_album(), unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    if uploaded_file:
        with col2:
            st.markdown(template_subheading('Uploaded Image', 'black', '#AED6F1'), unsafe_allow_html=True)
            st.image(uploaded_file)
            
            face_detected = True

            # Face detection branch
            if face_detected:
                st.markdown(template_subheading('박스 안쪽에 얼굴이 잘 위치해있나요?', 'black', '#AED6F1', '125%'), unsafe_allow_html=True)
                face_detect_true_btn = st.button('네')
                face_detect_false_btn = st.button('아니오')


    if uploaded_file2:
        with col3:
            st.markdown(template_subheading('Similar Actor', 'black', '#D5DBDB'), unsafe_allow_html=True)
            st.image(uploaded_file2)
            show_beautyGAN_btn = st.button('메이크업 결과 적용')
            st.markdown(bootstrap_block_level_button('메이크업 적용'), unsafe_allow_html=True)
            
    if uploaded_file and uploaded_file2 and show_beautyGAN_btn:
        # TODO: 이미지 View
        image_bytes = uploaded_file.getvalue() # binary 형식
        ref_bytes = uploaded_file2.getvalue() # binary 형식

        def crop_face(image_raw):
            return image_box

        no_makeup, makeup = transform_image(image_bytes, ref_bytes)
        files = [('files',(uploaded_file.name, image_bytes, uploaded_file.type)),
                ('files', (uploaded_file2.name, ref_bytes, uploaded_file2.type))]

        col1, col2, col3, col4, col5 = st.columns(5)

        with col2:
            st.subheader("Input Face")
            st.image(no_makeup)

        with col3:
            st.subheader("Makeup")
            st.image(makeup)
         
        with col4:
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
                st.success('성공!')


#%% Main part
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(
    page_title='배우고 싶니?', 
    layout="wide",
    )

main()

