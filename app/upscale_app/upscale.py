import base64
import cv2
import numpy
from cv2 import dnn_superres



# with open('lama_300px.png', 'rb') as image:
#     img_str = base64.b64encode(image.read()).decode()



# # convert string data to numpy array
# file_bytes = numpy.fromstring(filestr, numpy.uint8)
# # convert numpy array to image
# img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)


# CV2


def upscaler(img_str: bytes, output_path: str, model_path: str = 'EDSR_x2.pb') -> None:
    """
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :param model_path: путь к ИИ модели
    :return:
    """

    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)

    img_str = base64.b64decode(img_str.encode())

    nparr = numpy.fromstring(img_str, numpy.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1

    # image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)


def example():
    upscaler(img_str, 'lama_600px.png')


if __name__ == '__main__':
    example()
    