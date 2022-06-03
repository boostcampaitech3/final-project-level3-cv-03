#%% Set module configurations
import sys
import subprocess
from tabnanny import check

subprocess.check_call(["pip", "install", "-r", "requirements_crawl.txt"])
# !pip install '-r' 'requirements_crawl.txt'

subprocess.check_call(["apt-get", "install", "-y", "xvfb"])
# !apt-get install 'y' 'xvfb'

# Load modules
import selenium
import os
import requests
import urllib
import parmap
import itertools as it
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote_plus
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from multiprocessing import cpu_count

#%% Set multiprocessing configuration
cpu_use = cpu_count()-1 # round(2*cpu_count()/3)

#%% Install Chrome and set chrome configuration
# Download chrome
subprocess.check_call(["wget", "-N", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"])
# !wget -N https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install chrome
subprocess.check_call(['apt', 'install', './google-chrome-stable_current_amd64.deb', '-y'])
# !apt install ./google-chrome-stable_current_amd64.deb -y

# Check chrome version
subprocess.check_call(['google-chrome', '--version'])
# !google-chrome --version

# Download chrome driver
if 'chromedriver_linux64.zip' not in os.listdir():
    subprocess.check_call(['wget', '-N', 'https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_linux64.zip'])
    # !wget -N 'https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_linux64.zip'
    
# Unzip chrome driver
subprocess.check_call(['unzip', '-n', 'chromedriver_linux64.zip'])
# !unzip -n 'chromedriver_linux64.zip'

#%% Define custom functions
def check_image_appropriateness(img_size, boxes):
    if any((img_size[0] < 224, img_size[1] < 224)):
        check_img_size = False
    else:
        check_img_size = True

    if len(boxes) != 1:
        check_num_boxes = False
    else:
        check_num_boxes = True
        box_width, box_height = boxes[0][2] - boxes[0][0], boxes[0][3] - boxes[0][1]

    if check_num_boxes:
        if any((box_width < 224, box_height < 224)):
            check_box_size = False
        else:
            check_box_size = True
    
    return all((check_img_size, check_num_boxes, check_num_boxes))


def get_chrome_driver(custom_chrome_options=None):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=custom_chrome_options)
    return driver


def crawl_a_keyword(search_key,
                    actor_idx,
                    actor, 
                    num_total_actor,
                    max_img_cnt,
                    img_save_path, 
                    wrong_img_save_path,
                    save_wrong_image):    
    global cnt, wrong_cnt

    # Load face detection model
    mtcnn = MTCNN()

    with get_chrome_driver(custom_chrome_options) as driver:
        driver.implicitly_wait(3)
    
        # Get image search page by google
        driver.get('https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl')
        driver.implicitly_wait(3)
        
        # Query part
        element = driver.find_element(by=By.NAME, value='q')
        
        # Send search keyword
        element.send_keys(search_key)
        element.send_keys(Keys.RETURN)

        # Scroll down
        height = driver.execute_script("return document.body.scrollHeight") # Get maximum height
        while True:
            scroll_down_cnt = 0
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll down
            sleep(3) # wait for image load
            new_height = driver.execute_script("return document.body.scrollHeight")
            # print(f'old height {height} || new height {new_height}')
            
            if new_height == height:
                try:
                    driver.find_element(by=By.CSS_SELECTOR, value='./mye4qd').click()
                except:
                    break            
        
            if scroll_down_cnt > 1000:
                print('Scroll down iteration stopped due to iteration limit reached.')
            
            height = new_height
            scroll_down_cnt += 1
            
        # Get images
        imgs = driver.find_elements(by=By.CSS_SELECTOR, value='.rg_i.Q4LuWd')
        
        for img in imgs:
            if (cnt+1)%100 == 0:
                print(f'Actor [{actor}][{actor_idx+1}/{num_total_actor}] || count [{cnt+1}/{max_img_cnt}]')
            try:
                img.click()
                sleep(2)
                img_url = driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute(
                    'src')

                img_path = img_save_path + actor + f'_{str(cnt).zfill(3)}' + '.jpg'

                urlretrieve(img_url, img_path)

                # Load saved image
                img_saved = Image.open(img_path)
                img_size = img_saved.size

                # Detect faces in the loaded image
                boxes, _ = mtcnn.detect(img_saved)

                img_appropriateness = check_image_appropriateness(img_size, boxes)

                if img_appropriateness:
                    cnt += 1 # only count when there is only one big enough face in the image
                elif not img_appropriateness and save_wrong_image:           
                    wrong_img_path = wrong_img_save_path + actor + f'_{str(wrong_cnt).zfill(3)}' + '.jpg'

                    img_cp = img_saved.copy()
                    draw = ImageDraw.Draw(img_cp)

                    box_width, box_height = boxes[0][2] - boxes[0][0], boxes[0][3] - boxes[0][1]

                    # Draw red box in the image if there are more than one face in the image
                    for box in boxes:
                        draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6) # Draw face box
                        # draw.rectangle([box[0], box[1], box[3], box[2]], width=6, outline=(0, 0, 255)) # Test box

                    img_cp.save(wrong_img_path)

                    wrong_cnt += 1
                else:
                    print('Exceptional case')
                    pass

                if cnt >= max_img_cnt:
                    break
            except Exception as e:
                # print(e)
                pass


def crawl_an_actor(actor_idx: int, num_total_actor: int, actor: str, max_img_cnt: int, search_bases: list, save_wrong_image=False):
    global cnt, wrong_cnt

    # Make save directory
    if not os.path.isdir('./crawled_data'):
        os.mkdir('crawled_data')
    
    if save_wrong_image:
        if not os.path.isdir('./wrong_image'):
            os.mkdir('./wrong_image')

    img_save_path = f'./crawled_data/{actor}/'    
    if not os.path.isdir(img_save_path):
        os.mkdir(img_save_path)

    wrong_img_save_path = f'./wrong_image/{actor}/'
    if save_wrong_image:
        if not os.path.isdir(wrong_img_save_path):
            os.mkdir(wrong_img_save_path)

    # Log image count
    cnt = 0
    wrong_cnt = 0

    # Crawl images
    search_keys = [x.replace('[대체]', actor) for x in search_bases]

    for search_key in search_keys:
        crawl_a_keyword(search_key, 
                        actor_idx,
                        actor,
                        num_total_actor,
                        max_img_cnt,
                        img_save_path,
                        wrong_img_save_path,
                        save_wrong_image)
            
    print(f'---Crawling DONE. Actor [{actor}][{actor_idx+1}/{num_total_actor}] || Image [{cnt}/{max_img_cnt}]---')      
    if save_wrong_image:
        return actor, cnt, wrong_cnt
    else:
        return actor, cnt

    if save_wrong_image:
        df_wrong_log.loc[actor, :] = [wrong_cnt, max_img_cnt, 100*wrong_cnt/max_img_cnt]

#%% Crawl data
if __name__=='__main__':
    # Set driver option
    custom_chrome_options = webdriver.ChromeOptions()
    custom_chrome_options.add_argument('--headless')
    custom_chrome_options.add_argument('--no-sandbox')
    custom_chrome_options.add_argument("--single-process")
    custom_chrome_options.add_argument("--disable-dev-shm-usage")

    # Get crawling object
    max_img_cnt = 500
    save_wrong_image = True

    # Load actor names from csv file
    df_actors = pd.read_csv('드라마_리스트업.csv')
    actors_name_male = [actor.strip() for row in df_actors['남배우'].dropna() for actor in row.split(',')]
    actors_name_female = [actor.strip() for row in df_actors['여배우'].dropna() for actor in row.split(',')]

    actor_names = actors_name_female + actors_name_male
    actor_names = list(set(actor_names))
    num_total_actor = len(actor_names)

    search_bases = [
        '배우 [대체]',
        '배우 [대체] 시사회',
        '배우 [대체] 화보'
    ]

    # actor_idx: int, num_total_actor: int, actor: str, max_img_cnt: int, search_baese: list, save_wrong_image=False
    test_crawl_input = list(
        zip(
            np.arange(len(actor_names)),
            it.repeat(num_total_actor),
            actor_names,
            it.repeat(max_img_cnt),
            it.repeat(search_bases),
            it.repeat(save_wrong_image)
        )
    )

    # DataFrame for logging crawl
    df_crawl_log = pd.DataFrame(index=actor_names, columns=['done', 'goal', 'percent'])
    if save_wrong_image: df_wrong_log = pd.DataFrame(index=actor_names, columns=['done', 'goal', 'percent'])

    # Run parallel crawl
    crawl_rslt = parmap.starmap(
        crawl_an_actor,
        test_crawl_input,
        pm_pbar=True,
        pm_processes=cpu_use)

    for rslt in crawl_rslt:
        df_crawl_log.loc[rslt[0], :] = [rslt[1], max_img_cnt, 100*rslt[1]/max_img_cnt]

    df_crawl_log.to_csv('./crawled_data/crawling_result.csv')
    if save_wrong_image:
        for rslt in crawl_rslt:
            df_wrong_log.loc[rslt[0], :] = [rslt[2], max_img_cnt, 100*rslt[2]/max_img_cnt]

        df_wrong_log.to_csv('./wrong_image/wrong_result.csv')