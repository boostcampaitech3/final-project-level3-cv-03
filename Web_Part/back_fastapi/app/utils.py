from ast import Bytes
import base64
import PIL
import dlib
from PIL import Image
import numpy as np
import io, json, requests, random


detector = dlib.get_frontal_face_detector()  # 얼굴 영역 인식 모델 로드
sp = dlib.shape_predictor("./weights/shape_predictor_5_face_landmarks.dat")


def preprocess(img):
    return img / 127.5 - 1.0  # 0 ~ 255 -> -1 ~ 1


def postprocess(img):
    return (img + 1.0) * 127.5  # -1 ~ 1 -> 0 ~ 255


def align_faces(img):  # 원본이미지를 넣으면 align 완료된 얼굴이미지 반환하는 함수
    dets = detector(img, 1)
    objs = dlib.full_object_detections()

    for detection in dets:
        s = sp(img, detection)
        objs.append(s)
    faces = dlib.get_face_chips(img, objs, size=256, padding=0.35)

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


# reference image -> bytes_str
def ref_actor_image(actor : str):
    with open('actor_data.json', 'r', encoding="UTF-8") as f:
        json_data = json.loads(f.read())
    img_url = json_data[actor][random.randrange(0, 3)]
    ref_image = Image.open(requests.get(img_url, stream=True).raw)
    ref_bytes_str = from_image_to_bytes(ref_image)
    return ref_bytes_str