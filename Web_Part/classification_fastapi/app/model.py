#### mdoel.py ####
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision

#### predict.py ####
import streamlit as st
import numpy as np
import torch

#### utils.py (transform) ####
import io
import numpy as np
import cv2

import albumentations as A
from albumentations.pytorch import ToTensorV2
import torch


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#### mdoel.py ####
def efficientnet(celeb_num):
    model = torchvision.models.efficientnet_b7(pretrained = False)
    model.classifier[1] = nn.Linear(in_features=2560, out_features=celeb_num, bias=True)
    return model


#### predict.py ####
def get_prediction(model, image_bytes):
    
    img = transform_image(image_bytes=image_bytes).to(device)
    
    pred = model(img)
    pred = pred.to('cpu').argmax()
    
    return pred

# @st.cache
def load_model(celeb_num):
    ## model 불러오기
    saved_path = './app/model_saved/epoch_20.pt'

    # model = Efficientnet_b7(celeb_num=len(celeb_list)).to(device)
    model = efficientnet(celeb_num=celeb_num)
    model.load_state_dict(torch.load(saved_path, map_location=device))
    # model.to(device)
    
    return model


#### utils.py (transform) ####
def transform_image(image_bytes: bytes) -> torch.Tensor:
    test_transform = A.Compose([
                            A.Resize(256,256),
                            ToTensorV2()
                            ])
    img_ = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_, cv2.IMREAD_COLOR)    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
    img /= 255.0

    return test_transform(image=img)['image'].unsqueeze(0)