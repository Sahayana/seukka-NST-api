
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
from config import NstappConfig


def load_style(path_to_style, max_dim):
    img = tf.io.read_file(path_to_style)
    img = tf.image.decode_image(img, channels= 3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim
    
    #이미지 사이즈이기떄문에 정수형으로 전환
    new_shape = tf.cast(shape * scale, tf.int32)
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

def upload_tesor_img(bucket, tensor, key):
    tensor = np.array(tensor*255, dtype=np.uint8)
    image = Image.fromarray(tensor[0])
    buffer = BytesIO()
    image.save(buffer, 'PNG')
    buffer.seek(0)
    NstappConfig.s3.put_object(Bucket=bucket, Key=key, Body=buffer, ACL='public-read')
    location = NstappConfig.s3.get_bucket_location(Bucket=bucket)['LocationConstraint']
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket, key)
    return url

def nst_apply(key: str, img) -> str:

    # 원하는
    style_path = tf.keras.utils.get_file('kkm.jpg',
                                        'https://tekken.s3.ap-northeast-2.amazonaws.com/kkm.jpg')
    style_path_2 = tf.keras.utils.get_file('border.jpg',
                                        'https://tekken.s3.ap-northeast-2.amazonaws.com/border.jpg')
    style_image_first = load_style(style_path, 128)
    style_image_second = load_style(style_path_2, 512)
    style_image_third = load_style(style_path, 512)
    style_image_fourth = load_style(style_path, 1024)
    # style_image_2 = load_style(style_path_2, 256)
    img = Image.open(img.file).convert('RGB')
    content_image = tf.keras.preprocessing.image.img_to_array(img)
    content_image = content_image.astype(np.float32)[np.newaxis, ...] / 255
    content_image = tf.image.resize(content_image, (256,512))

    


    stylized_img = NstappConfig.hub_module(tf.constant(content_image), tf.constant(style_image_second))[0]



    # stylized_img_1 = NstappConfig.hub_module(tf.constant(content_image), tf.constant(style_image_first))[0][:, 0:64]
    # stylized_img_2 = NstappConfig.hub_module(tf.constant(content_image), tf.constant(style_image_second))[0][:, 64:128]
    # stylized_img_3 = NstappConfig.hub_module(tf.constant(content_image), tf.constant(style_image_third))[0][:, 128:192]
    # stylized_img_4 = NstappConfig.hub_module(tf.constant(content_image), tf.constant(style_image_fourth))[0][:, 192:256]
    # # stylized_img_2 = NstappConfig.hub_module(tf.constant(content_image), tf.constant(style_image_2))[0][:, 130:256]
    # # stylized_img = np.concatenate([stylized_img_1, stylized_img_2, stylized_img_3, stylized_img_4], axis = 1)

    image_url = upload_tesor_img('baenst', stylized_img, key)
    return image_url

