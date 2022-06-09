from xmlrpc.client import Boolean
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision

#### predict.py, utils.py (transform) ####
import streamlit as st
import numpy as np
import io, cv2
from ast import Bytes
import PIL
from PIL import Image
import base64
import math
import albumentations as A
from albumentations.pytorch import ToTensorV2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

def from_bytes_to_numpy(image_bytes :bytes):
    numpy_ = np.frombuffer(image_bytes, dtype=np.uint8) ## 1차원 numpy 배열로
    nparray = cv2.imdecode(numpy_, cv2.IMREAD_COLOR) ## 3차원 numpy 배열로
    nparray = cv2.cvtColor(nparray, cv2.COLOR_BGR2RGB).astype(np.float32) ## RGB변환 및 자료형 변환
    return nparray
    
#### mdoel.py ####
def efficientnet(celeb_num):
    model = torchvision.models.efficientnet_b4(pretrained=False)
    # model.classifier[1] = nn.Linear(in_features=2560, out_features=celeb_num, bias=True)
    model.classifier[1] = nn.Linear(in_features=1792, out_features=celeb_num, bias=True)
    return model


#### predict.py ####
def get_prediction(model, image_bytes):
    device = torch.device('cpu')
    img = transform_image(image_bytes=image_bytes).to(device)
    pred = model(img)
    percentage = F.softmax(pred, dim=1).max().item()
    pred_index = pred.to("cpu").argmax()
    return pred_index, percentage


# @st.cache
def load_model(celeb_num=175):
    ## model  storage에서 불러오기
    saved_path = "./models/efficientnet/weights/efficientnet_b4_epoch_28.pt"
    # model = Efficientnet_b7(celeb_num=len(celeb_list)).to(device)
    model = efficientnet(celeb_num=celeb_num)
    model.load_state_dict(torch.load(saved_path, map_location=device))
    # model.to(device)
    return model

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
        if isin > 0 and isin < image_size:
            flag = True
            break
    warped = cv2.warpAffine(img, M, (image_size, image_size), borderValue=0.0)
    return warped, image_box, flag

#### utils.py (transform) ####
def transform_image(image_bytes: bytes) -> torch.Tensor:
    img = from_bytes_to_numpy(image_bytes)
    img /= 255.0
    test_transform = A.Compose([ToTensorV2()])
    return test_transform(image=img)["image"].unsqueeze(0)


def convert_image(image_bytes: bytes):
    try:
            
        img = from_bytes_to_numpy(image_bytes)
        boxes_raw = app.get(img)
        if len(boxes_raw) == 0:

            return len(boxes_raw), ''

        elif len(boxes_raw) >= 1:
            max_area = 0
            max_index = -1
            for index, box in enumerate(boxes_raw):
                bbox = box['bbox']
                if max_area < (bbox[2]-bbox[0]) * (bbox[3]-bbox[1]):
                    max_area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1])
                    max_index = index
            boxes = boxes_raw[max_index]

            img, image_box, flag = norm_crop(img = img, landmark = boxes['kps'], image_size = CROPPED_IMG_SIZE, mode = 'NOMODE!') ## mode = 'arcface'
            if flag is True: ##이미지 모서리에 공백이 있는 경우 
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
            
                if output.shape[0] < 380:
                    img = cv2.resize(output, dsize=(380, 380),interpolation = cv2.INTER_LINEAR)
                else: 
                    img = cv2.resize(output, dsize=(380, 380),interpolation = cv2.INTER_AREA)
            else:
                img = cv2.resize(img, dsize=(380, 380), interpolation=cv2.INTER_AREA)
            img = img.astype(np.uint8)
            pil_image = Image.fromarray(img)
            output_img_bytes = from_image_to_bytes(pil_image)

            return len(boxes_raw), output_img_bytes
        else:
            ## 이러면 안되는거아닌가##
            return 0, ''
    except:
        return 0, ''