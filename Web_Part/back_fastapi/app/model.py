from ast import Bytes
from tkinter import Image
import tensorflow as tf
import numpy as np
from back_fastapi.app.utils import transform_image, from_image_to_bytes

from PIL import Image


def preprocess(img):
    return img.astype(np.float32) / 127.5 - 1.0  # 0 ~ 255 -> -1 ~ 1


def postprocess(img):
    return ((img + 1.0) * 127.5).astype(np.uint8)  # -1 ~ 1 -> 0 ~ 255


def get_beautygan(moedl_path: str = "./models/model.meta"):
    # 세션 생성
    sess = tf.Session()    
    sess.run(tf.global_variables_initializer())
    
    # 모델의 그래프를 불러오기
    saver = tf.train.import_meta_graph(moedl_path)
    
    # 모델의 weighs를 load
    saver.restore(sess, tf.train.latest_checkpoint("./models"))
    # 그래프에 저장
    graph = tf.get_default_graph()
    
    return sess, graph


def transfer(sess, graph, image_bytes: bytes, ref_bytes: bytes) -> Bytes:
    X = graph.get_tensor_by_name("X:0")  # source
    Y = graph.get_tensor_by_name("Y:0")  # reference
    Xs = graph.get_tensor_by_name("generator/xs:0")  # output

    img, reference = transform_image(image_bytes, ref_bytes)

    X_img = preprocess(img)
    X_img = np.expand_dims(X_img, axis=0)
    
    Y_img = preprocess(reference)
    Y_img = np.expand_dims(Y_img, axis=0)

    output = sess.run(Xs, feed_dict={X: X_img, Y:Y_img})
    output_img = postprocess(output[0])

    pil_image = Image.fromarray(output_img) # ndarray -> pillow image
    output_img_bytes = from_image_to_bytes(pil_image)

    return output_img_bytes
