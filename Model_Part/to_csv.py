import pandas as pd
import random
from pathlib import Path


SEED = 42
############ Custom ############
PORTION = 20  ## 몇퍼센트(백분율)를 validation으로 사용할 것인지
IMG_DIR_PATH = '/opt/ml/Cropped1024_det256_min60_FIRST'
############ Custom ############

random.seed(SEED)
train_list = []
valid_list = []
actor_list = []
num_actor_list = []

for actor in Path(IMG_DIR_PATH + '/images').iterdir():

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

    actor_list.append([actor.name])
    num_actor_list.append([len(valid_path_list), len(train_path_list), len(train_path_list) + len(valid_path_list), actor.name])


df_train = pd.DataFrame(data=train_list, columns = ['path','name'])
df_train.to_csv(IMG_DIR_PATH+'/train.csv')

df_valid = pd.DataFrame(data=valid_list, columns = ['path','name'])
df_valid.to_csv(IMG_DIR_PATH+'/valid.csv')

df_actor = pd.DataFrame(data=actor_list, columns = ['name'])
df_actor.to_csv(IMG_DIR_PATH+'/actor.csv')

df_num_actor = pd.DataFrame(data=num_actor_list, columns = ['valid_num', 'train_num', 'total_num', 'name'])
df_num_actor.to_csv(IMG_DIR_PATH+'/num_actor.csv')