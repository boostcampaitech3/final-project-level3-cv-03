from xmlrpc.client import Boolean
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision

#### predict.py, utils.py (transform) ####
import streamlit as st
import numpy as np
import io, cv2

import albumentations as A
from albumentations.pytorch import ToTensorV2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
    pred = pred.to("cpu").argmax()
    return pred


# @st.cache
def load_model(celeb_num=175):
    ## model  storage에서 불러오기
    saved_path = "./models/efficientnet/weights/efficientnet_b4_epoch_28.pt"
    # model = Efficientnet_b7(celeb_num=len(celeb_list)).to(device)
    model = efficientnet(celeb_num=celeb_num)
    model.load_state_dict(torch.load(saved_path, map_location=device))
    # model.to(device)
    return model


#### utils.py (transform) ####
def transform_image(image_bytes: bytes, get_box: Boolean=False) -> torch.Tensor:
    img_ = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
    boxes_raw = app.get(img)
    boxes = boxes_raw[0]
    img = norm_crop(img = img, landmark = boxes['kps'], image_size = CROPPED_IMG_SIZE, mode = 'NOMODE!') ## mode = 'arcface'
    img /= 255.0
    test_transform = A.Compose([A.Resize(380, 380), ToTensorV2()])
    if get_box:
        return test_transform(image=img)["image"].unsqueeze(0), boxes_raw
    else:
        return test_transform(image=img)["image"].unsqueeze(0)
