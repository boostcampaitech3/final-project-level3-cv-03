from ast import Bytes
import base64
import PIL
from PIL import Image
import numpy as np
import io, json, requests, random, cv2, math

import albumentations as A

import insightface
from insightface.utils.face_align import *
from insightface.utils.face_align import norm_crop as norm_crop
from insightface.utils.face_align import estimate_norm as estimate_norm
from insightface.app import FaceAnalysis

CROPPED_IMG_SIZE = 1024 ##

insightface.utils.face_align.src_map = {
    256 : insightface.utils.face_align.src * 256 / 112,
    380 : insightface.utils.face_align.src * 380 / 112,
    1024 : insightface.utils.face_align.src * 1024 / 112
}

app = FaceAnalysis(allowed_modules=['detection'], providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(256, 256))

def preprocess(img):
    return img / 127.5 - 1.0  # 0 ~ 255 -> -1 ~ 1


def postprocess(img):
    return (img + 1.0) * 127.5  # -1 ~ 1 -> 0 ~ 255

def norm_crop(img, landmark, image_size=112, mode='arcface'):
    M, pose_index = estimate_norm(landmark, image_size, mode)

    candidates = [(0, 0), (0, img.shape[1]), (img.shape[0], 0), (img.shape[0], img.shape[1])]

    xs, ys = [], []
    for y, x in candidates:
        a = M[0 , 0] * x + M[0, 1] * y + M[0, 2]
        b = M[1 , 0] * x + M[1, 1] * y + M[1, 2]
        xs.append(a)
        ys.append(b)

    image_box = [math.floor(min(ys)), math.ceil(max(ys)), math.floor(min(xs)), math.ceil(max(xs))]
    if image_box[0] < 0:
        image_box[0] = 0
    if image_box[1] > image_size:
        image_box[1] = image_size
    if image_box[2] < 0:
        image_box[2] = 0
    if image_box[3] > image_size:
        image_box[3] = image_size

    flag = False ## 얼굴 이미지가 전체 크기보다 작은지
    for isin in image_box:
        if isin >= 0 and isin <= image_size:
            flag = True
            break
    warped = cv2.warpAffine(img, M, (image_size, image_size), borderValue=0.0)
    return warped, image_box, flag


def align_faces(img):  # 원본이미지를 넣으면 align 완료된 얼굴이미지 반환하는 함수
    boxes_raw = app.get(img)
    
    max_area = 0
    max_index = -1
    for index, box in enumerate(boxes_raw):
        bbox = box['bbox']
        if max_area < (bbox[2]-bbox[0]) * (bbox[3]-bbox[1]):
            max_area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1])
            max_index = index
    boxes = boxes_raw[max_index]

    img, image_box, flag = norm_crop(img = img, landmark = boxes['kps'], image_size = CROPPED_IMG_SIZE, mode = 'NOMODE!') ## mode = 'arcface'
    if flag is True: ##이미지가 380x380보다 작은경우 
        w = image_box[3] -image_box[2]
        h = image_box[1] -image_box[0]
        diff = math.floor(abs(w-h) / 2)
        output = None
        if w > h:
            if (w-h) % 2 ==1:
                output = img[image_box[0]-diff : image_box[1]+diff, image_box[2] : image_box[3]-1]
            else:
                output = img[image_box[0]-diff : image_box[1]+diff, image_box[2] : image_box[3]]
        elif w < h:
            if (w-h) % 2 ==1:
                output = img[image_box[0] : image_box[1]-1, image_box[2]-diff : image_box[3]+diff]
            else:
                output = img[image_box[0] : image_box[1],   image_box[2]-diff : image_box[3]+diff]
        else:
            output = img[image_box[0] : image_box[1], image_box[2] : image_box[3]]
        if output.shape[0] < 256:
            img = cv2.resize(output, dsize=(256, 256),interpolation = cv2.INTER_LINEAR)
        else: 
            img = cv2.resize(output, dsize=(256, 256),interpolation = cv2.INTER_AREA)
    else:
        img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_AREA)
    return img

def transform_image(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")
    image_array = np.array(image)
    img = align_faces(image_array)
    return img

def from_image_to_bytes(img: PIL.Image) -> Bytes:
    """
    pillow image 객체를 bytes로 변환
    """
    # Pillow 이미지 객체를 Bytes로 변환
    imgByteArr = io.BytesIO() # <class '_io.BytesIO'>
    img.save(imgByteArr, format="jpeg") # PIL 이미지를 binary형태의 이름으로 저장
    imgByteArr = imgByteArr.getvalue() # <class 'bytes'>
    # Base64로 Bytes를 인코딩
    encoded = base64.b64encode(imgByteArr) # <class 'bytes'>
    # Base64로 ascii로 디코딩
    decoded = encoded.decode("ascii") # <class 'str'>
    
    return decoded

# reference image -> bytes_str
def ref_actor_image(predict : int):
    with open('actor.json', 'r', encoding="UTF-8") as f:
        json_data = json.loads(f.read())
    actor_list = [actor_data for actor_data in json_data["actor"] if actor_data["id"] == predict]
    actor_images = actor_list[0]["image"]
    img_url = actor_images[random.randrange(0, len(actor_images))]
    ref_image = Image.open(requests.get(img_url, stream=True).raw)
    ref_bytes_str = from_image_to_bytes(ref_image)
    return ref_bytes_str, actor_list[0]["name"], img_url
