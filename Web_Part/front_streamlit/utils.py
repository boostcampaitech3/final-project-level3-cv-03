from ast import Bytes
import base64
import PIL
# import dlib
from PIL import Image
import numpy as np
import io

import insightface
from insightface.utils.face_align import *
from insightface.utils.face_align import norm_crop as norm_crop
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
CROPPED_IMG_SIZE = 1024 ##


insightface.utils.face_align.src_map = {
    256 : insightface.utils.face_align.src * 256 / 112,
    380 : insightface.utils.face_align.src * 380 / 112,
    1024 : insightface.utils.face_align.src * 1024 / 112
}

app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(256, 256))


def preprocess(img):
    return img / 127.5 - 1.0  # 0 ~ 255 -> -1 ~ 1


def postprocess(img):
    return (img + 1.0) * 127.5  # -1 ~ 1 -> 0 ~ 255


def align_faces(img):  # 원본이미지를 넣으면 align 완료된 얼굴이미지 반환하는 함수

    boxes = app.get(img)
    boxes = boxes[0]
    abc = norm_crop(img = img, landmark = boxes['kps'], image_size = CROPPED_IMG_SIZE, mode = 'NOMODE!') ## mode = 'arcface'
    abc = cv2.resize(abc, (256, 256), interpolation= cv2.INTER_AREA)
    faces = []
    faces.append(abc)
    return faces


def transform_image(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")
    image_array = np.array(image)
    img = align_faces(image_array)[0]
    return img


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
