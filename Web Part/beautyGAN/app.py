import streamlit as st
import tensorflow as tf
import numpy as np

import dlib
import io
import cv2
from PIL import Image
from utils import align_faces

# grid
from typing import List, Optional
import markdown
import pandas as pd

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")


def preprocess(img):
    return img.astype(np.float32) / 127.5 - 1.0  # 0 ~ 255 -> -1 ~ 1


def postprocess(img):
    return ((img + 1.0) * 127.5).astype(np.uint8)  # -1 ~ 1 -> 0 ~ 255


def main():
    
    st.title("BeautyGAN Prototype")

    # grid
    col1,col2 = st.columns(2) 
    with col1:
      # TODO: File Uploader 구현
      uploaded_file = st.file_uploader("Choose no_makeup image", type=["jpg", "jpeg", "png"])
      # uploaded_file

      if uploaded_file:
          # TODO: 이미지 View
          image_bytes = uploaded_file.getvalue() # binary 형식
          image = Image.open(io.BytesIO(image_bytes)) # Binary 형태의 이미지 데이터를 decode       
          # st.image(image, caption="Uploaded Image")
          # st.write(io.BytesIO(image_bytes))

          image = image.convert('RGB')
          image_array = np.array(image)
          no_makeup = align_faces(image_array)[0]
          # st.image(no_makeup)

    with col2:
      uploaded_file2 = st.file_uploader("Choose makeup image", type=["jpg", "jpeg", "png"])
      # uploaded_file2

      if uploaded_file2:
          # TODO: 이미지 View
          ref_bytes = uploaded_file2.getvalue() # binary 형식
          image_ref = Image.open(io.BytesIO(ref_bytes)) # Binary 형태의 이미지 데이터를 decode       
          # st.image(image, caption="Uploaded Image")
          # st.write(io.BytesIO(image_bytes))

          image_ref = image_ref.convert('RGB')
          image_ref_array = np.array(image_ref)
          makeup = align_faces(image_ref_array)[0]
          # st.image(makeup, caption="makeup image")

    # BeautyGAN load
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    saver = tf.train.import_meta_graph("models/model.meta")
    saver.restore(sess, tf.train.latest_checkpoint("models"))
    graph = tf.get_default_graph()

    X = graph.get_tensor_by_name("X:0")  # source
    Y = graph.get_tensor_by_name("Y:0")  # reference
    Xs = graph.get_tensor_by_name("generator/xs:0")  # output
    
    # Inference
    if uploaded_file and uploaded_file2: 
      X_img = preprocess(no_makeup)
      X_img = np.expand_dims(X_img, axis=0)
      
      Y_img = preprocess(makeup)
      Y_img = np.expand_dims(Y_img, axis=0)

      output = sess.run(Xs, feed_dict={X: X_img, Y:Y_img})
      output_img = postprocess(output[0])

      # st.image(output_img,caption="Result!!!")
      images = [no_makeup, makeup, output_img]
      caption=['no makeup', 'makeup', 'Result!']
      _, show1,_,show2,_,show3,_ = st.columns([1,3,1,3,1,3,1])
      with show1:
        st.image(images[0], caption[0])
      with show2:
        st.image(images[1], caption[1])
      with show3:
        st.image(images[2], caption[2])

main()