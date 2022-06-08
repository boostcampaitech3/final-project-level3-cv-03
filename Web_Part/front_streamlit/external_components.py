import streamlit as st
from urllib import parse

def set_bg_hack_url():
    st.markdown(
         f"""
         <style>
            @import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&display=swap');
        </style>
         """,
         unsafe_allow_html=True
     )

    
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


def bootstrap_intro(texts: list):
    return f"""
        <div class="home-intro-div">
            <div class="home-intro-wrapper">
                <span class="home-intro">
                    {texts[0]}
                </span>
                <span class="home-intro">
                    {texts[1]}
                </span>
            </div>
            <div class="home-intro-wrapper">
                <span class="home-intro">
                    {texts[2]}
                </span>
                <span class="home-intro">
                    {texts[3]}
                </span>
            </div>
        </div>
        """


def bootstrap_navbar():
    return """
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand like-a-actor" href="#">배우고 싶니?</a>
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
          <h3 class="masthead-brand">배우고 싶니 v1.1.0</h3>
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
    <h1  class="like-a-actor" style="text-align:center; color:white; font-weight:bold; font:sans serif">{head_title}</h1>
    """


def template_subheading(text: str, color: str='black', background_color: str=None):
    return f"""
    <h2 class="template-subheading" style="text-align:center; color:{color}; background-color:{background_color}; ">{text}</h2>
    """

def photo_subheading(text: str, color: str='black', background_color: str=None):
    return f"""
    <h2 class="template-subheading photo-heading" style="text-align:center; color:{color}; background-color:{background_color}; ">{text}</h2>
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
        <script language="javascript">
            function shareLink() {
                console.log('hello')
                Kakao.Link.sendScrap({
                    requestUrl: location.href
                });
            };
        </script>
        
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
# def apply_kakaotalk_button():
#     st.markdown("""
#     <style>
#     div.stButton > button:first-child {
#         background: url('https://developers.kakao.com/assets/img/about/logos/kakaotalksharing/kakaotalk_sharing_btn_medium.png') no-repeat;
#         height: 4.5em;
#         width: 4.5em;
#         border-radius:10px;
#         border:0px solid #000000;
#         margin: auto;
#         display: block;
#     }
#     div.stButton > button:hover {
#         background:linear-gradient(to bottom, #ce1126 5%, #ff5a5a 100%);
#         background-color:#ce1126;
#     }
#     div.stButton > button:active {
#         position:relative;
#         top:3px;
#     }
#     </style>""", unsafe_allow_html=True)


def footer_button(link):
    return f"""
    <div class="btn-footer">
        <a class="google-form-button" href="{link}">
        <span class="google-form-button-text">
        설문지 작성
        </span>
        </a>
    </div>
    """
def footer():
    return """
    <footer class="bittcoin-footer">
        <span class="bittcoin-footer-p">2022 Naver AI Boostcamp 3rd-CV-03 made by BittCoin
        </span>
        <span class="bittcoin-footer-p">(강면구, 김대근, 박선혁, 정재욱, 한현진)
        </span>
    </footer>
    """