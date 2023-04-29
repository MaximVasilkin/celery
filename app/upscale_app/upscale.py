import base64
import cv2
import numpy
from cv2 import dnn_superres


def upscaler(img_str: str, output_path: str, model_path: str = 'EDSR_x2.pb') -> None:
    '''
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :param model_path: путь к ИИ модели
    :return:
    '''

    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel('edsr', 2)

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
