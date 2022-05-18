import cv2
import glob
from PIL import Image, ImageDraw
import random
from facenet_pytorch import MTCNN
from pathlib import Path

############ Custom ############
SEED = 42
IMG_DIR_PATH = '/opt/ml/sample_data/images'
CROP_IMG_DIR_PATH = '/opt/ml/sample_data/crop_images' ## 크롭한 이미지들이 저장될 경로 지정
ENLARGE_MIN_RATIO = 1.6 ## CROP할 최소 배율
ENLARGE_MAX_RATIO = 2.1 ## CROP할 최대 배율
############ Custom ############


random.seed(SEED)
crop_root = Path(CROP_IMG_DIR_PATH)
mtcnn = MTCNN()

if ENLARGE_MIN_RATIO > ENLARGE_MAX_RATIO:
    print("적합한 배율을 설정하세요") 
for actor in Path(IMG_DIR_PATH).iterdir():
    if not actor.is_dir():
        continue
    crop_actor_dir_path = (Path(crop_root) / actor.name)
    crop_actor_dir_path.mkdir(parents=True, exist_ok=True)

    for image in actor.glob("*.jpg"):
        img_saved = Image.open(image)
        img_size = img_saved.size
        boxes, _ = mtcnn.detect(img_saved)

        if boxes is None:
            continue
        if len(boxes) >= 2:
            print("#####################################")
            continue

        img_cp = img_saved.copy()
        draw = ImageDraw.Draw(img_cp)

        # Draw red box in the image if there are more than one face in the image
        box = boxes[0]
        center_x, center_y =  (box[0] + box[2]) / 2, (box[1] + box[3]) / 2 ## 중심점 찾기
        ratio = ENLARGE_MIN_RATIO + random.random() * (ENLARGE_MAX_RATIO-ENLARGE_MIN_RATIO) ## 박스를 특정 비율로 확대
        new_width, new_height = ratio * (box[2]-box[0]) / 2,  ratio * (box[3]-box[1]) / 2
        new_box = [center_x - new_width, center_y - new_height, center_x + new_width, center_y + new_height]

        if new_width < 80 or new_height < 80:
            continue
        if box[0] >= box[2] or box[1] >= box[2]:
            print("what?WAEFW?FWEA?")
            continue
        ##crop이 경계를 넘어가지 않게
        if new_box[0] < 0: 
            new_box[0] = 0
        if new_box[1] < 0: 
            new_box[1] = 0
        if new_box[2] > img_size[0]: 
            new_box[2] = img_size[0]
        if new_box[3] > img_size[1]: 
            new_box[3] = img_size[1]

        crop_img = img_cp.crop(new_box)
        print(image)
        print(img_size)
        print(new_box)

        crop_img.save(crop_root / actor.name / image.name)