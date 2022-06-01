import cv2
import random
from pathlib import Path
from tqdm import tqdm
import insightface
from insightface.utils.face_align import *
from insightface.utils.face_align import norm_crop as norm_crop
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

SEED = 42
IMG_DIR_PATH = '/opt/ml/cleaned_v1/images' ## 이미지를 가져올 경로 지정!

############ Custom ############
CROPPED_IMG_SIZE = 1024  ## 저장될 이미지 사이즈 (가로 and 세로)
MIN_SIZE = 60           ## 최소 얼굴 사이즈 (가로 and 세로)
NAME = 'FIRST'          ## 폴더명 => ex) cropped_det256_min60_FIRST
DET_SIZE = 256          ## 숫자를 높이면 작은 얼굴들이 잘 탐지가 안되고, 낮추면 큰 얼굴이 감지가 안됩니다.
############ Custom ############

random.seed(SEED)

## 폴더 생성
cropped_dir_name = Path('/opt/ml/Cropped'+str(CROPPED_IMG_SIZE)+'_det' + str(DET_SIZE)+'_min'+str(MIN_SIZE) + '_' + NAME)
cropped_dir_name.mkdir(parents=False, exist_ok=True)
CROP_IMG_DIR_PATH = (cropped_dir_name / 'images') 
NOFACE_IMG_DIR_PATH = (cropped_dir_name / 'noface')
TOO_MANY_FACE_IMG_DIR_PATH = (cropped_dir_name / 'manyface')
CROP_IMG_DIR_PATH.mkdir(parents=False, exist_ok=True)
NOFACE_IMG_DIR_PATH.mkdir(parents=False, exist_ok=True)
TOO_MANY_FACE_IMG_DIR_PATH.mkdir(parents=False, exist_ok=True)

##insightface 초기 설정
insightface.utils.face_align.src_map = {CROPPED_IMG_SIZE : insightface.utils.face_align.src * CROPPED_IMG_SIZE / 112}
app = FaceAnalysis(allowed_modules=['detection'], providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(DET_SIZE, DET_SIZE))

count= 170
for index, actor in tqdm(enumerate(Path(IMG_DIR_PATH).iterdir())):
    print(actor.name)
    if index < count:
        continue
    if not actor.is_dir():
        continue
    crop_actor_dir_path = CROP_IMG_DIR_PATH / actor.name
    crop_actor_dir_path.mkdir(parents=False, exist_ok=True)

    for image in actor.glob("*.jpg"):
        img = ins_get_image(str(image)[:-4], to_rgb=True)
        print(image.name)
        boxes = app.get(img)

        satisfied_boxes = []
        for box in boxes:
            bbox = box['bbox']
            if bbox[2]-bbox[0]>=MIN_SIZE and bbox[3]-bbox[1]>=MIN_SIZE:
                satisfied_boxes.append(box)
        boxes = satisfied_boxes

        if boxes is None or len(boxes) == 0:
            img_path = str(NOFACE_IMG_DIR_PATH / image.name)
            cv2.imwrite(img_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            print("NONENONENONENONENONENONENONENONENONENONENONENONENONENONE")
            continue

        if len(boxes) >= 2:
            satisfied_boxes = []
            rimg = app.draw_on(img, boxes)
            img_path = str(TOO_MANY_FACE_IMG_DIR_PATH / image.name)
            cv2.imwrite(img_path, cv2.cvtColor(rimg, cv2.COLOR_RGB2BGR))
            print("TOOMANYTOOMANYTOOMANYTOOMANYTOOMANYTOOMANYTOOMANYTOOMANY")
            continue

        if len(boxes) == 1:
            boxes = boxes[0]
            bbox = boxes['bbox']
            abc = norm_crop(img = img, landmark = boxes['kps'], image_size = CROPPED_IMG_SIZE, mode = 'NOMODE!') 
            ## mode = 'arcface'로 바꿀 수 있음! arcface를 적용하면 조금 더 얼굴을 좁게 크롭함
            img_path = str(CROP_IMG_DIR_PATH / actor.name / image.name)
            cv2.imwrite(img_path, cv2.cvtColor(abc, cv2.COLOR_RGB2BGR))

        else:
            print("WTF??????????????????????????????")
            break