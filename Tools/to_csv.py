import pandas as pd
import random
from pathlib import Path

############ Custom ############
PORTION = 20  ## 몇퍼센트(백분율)를 validation으로 사용할 것인지
SEED = 42
IMG_DIR_PATH = '/opt/ml/sample_data/images'
TRAIN_CSV_PATH = "./train.csv"
VALID_CSV_PATH = "./valid.csv"
############ Custom ############

random.seed(SEED)
train_list = []
valid_list = []

for actor in Path(IMG_DIR_PATH).iterdir():
    if not actor.is_dir():
        continue
    image_path_list = []
    count = 0
    for image in actor.glob("*.jpg"):
        count += 1
        image_path_list.append(str(Path('').joinpath(*image.parts[-3: ])))

    random.shuffle(image_path_list)

    valid_num = count*PORTION // 100
    train_path_list = sorted(image_path_list[valid_num:])
    valid_path_list = sorted(image_path_list[:valid_num])

    for image in train_path_list:
        train_list.append([image, actor.name])

    for image in valid_path_list:
        valid_list.append([image, actor.name])


df_train = pd.DataFrame(data=train_list, columns = ['path','name'])
df_train.to_csv(TRAIN_CSV_PATH) ## train csv파일 위치 지정

df_valid = pd.DataFrame(data=valid_list, columns = ['path','name'])
df_valid.to_csv(VALID_CSV_PATH) ## valid csv파일이 저장될 위치 지정