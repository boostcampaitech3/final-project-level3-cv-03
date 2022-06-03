from ast import Bytes
import base64
import PIL
from PIL import Image
import io

def preprocess(img):
    return img / 127.5 - 1.0  # 0 ~ 255 -> -1 ~ 1


def postprocess(img):
    return (img + 1.0) * 127.5  # -1 ~ 1 -> 0 ~ 255


def from_image_to_bytes(img: PIL.Image) -> Bytes:
    """
    pillow image 객체를 bytes로 변환
    """
    # Pillow 이미지 객체를 Bytes로 변환
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format="jpeg")
    imgByteArr = imgByteArr.getvalue()
    # Base64로 Bytes를 인코딩
    encoded = base64.b64encode(imgByteArr)
    # Base64로 ascii로 디코딩
    decoded = encoded.decode("ascii")

    return decoded

# bytes_str -> image
def convert_bytes_to_image(bytes_str : str):
    str_to_bytes = base64.b64decode(bytes_str)
    image = Image.open(io.BytesIO(str_to_bytes))
    return image
