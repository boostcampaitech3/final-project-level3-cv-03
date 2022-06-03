import json
from collections import OrderedDict

# 배우 목록
with open('./actor_text.txt', 'r') as f:
    list_file = f.readlines()
list_file = [line.rstrip('\n') for line in list_file] 

# 이미지 파일 이름 가져오기
with open('./actor_image_list.txt', 'r') as f:
    image_file = f.readlines()
image_file = [line.rstrip('\n') for line in image_file] 

print(list_file[0].split(',')[1])

result = []
for i in range(len(list_file)):
    file_data = {}
    file_data["id"] = i
    file_data["name"] = f"{list_file[i].split(',')[1]}"
    file_data["name_en"]=f"{list_file[i].split(',')[2]}"
    file_data["image"] = []
    for image in image_file:
        if list_file[i].split(',')[2] == image.split('_')[0]:
            file_data["image"].append(f'https://storage.googleapis.com/bitcoin_images_storage/actor_en/{image}')
    
    result.append(file_data)
# print(json.dumps(file_data,ensure_ascii=False, indent="\t"))

with open('actor_make.json', 'w', encoding="utf-8") as make_file:
    json.dump(result, make_file, ensure_ascii=False, indent="\t")