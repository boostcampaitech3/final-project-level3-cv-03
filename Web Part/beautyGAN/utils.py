import io
import numpy as np
from PIL import Image

import albumentations
import albumentations.pytorch
import torch
import dlib

detector = dlib.get_frontal_face_detector() #얼굴 영역 인식 모델 로드
sp = dlib.shape_predictor('models/shape_predictor_5_face_landmarks.dat')

def align_faces(img):  #원본이미지를 넣으면 align 완료된 얼굴이미지 반환하는 함수
    dets = detector(img, 1)
    
    objs = dlib.full_object_detections()

    for detection in dets:
        s = sp(img, detection)
        objs.append(s)
        
    faces = dlib.get_face_chips(img, objs, size=256, padding=0.35)
    
    return faces