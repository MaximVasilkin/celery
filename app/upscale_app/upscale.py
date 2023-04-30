import base64
import cv2
import numpy
from cv2 import dnn_superres
from functools import lru_cache
from config import PATH_TO_MODEL


@lru_cache()
def get_model(model_path: str = PATH_TO_MODEL):
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel('edsr', 2)
    return scaler


def upscaler(img_str: str, output_path: str) -> None:
    '''
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :return:
    '''

    scaler = get_model()

    img_str = base64.b64decode(img_str.encode())
    nparr = numpy.fromstring(img_str, numpy.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1

    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)


def example():
    with open('lama_300px.png', 'rb') as image:
        image = base64.b64encode(image.read()).decode()
        upscaler(image, 'lama_600px.png')


if __name__ == '__main__':
    example()
