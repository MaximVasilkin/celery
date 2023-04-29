import requests
import time
import os


CURRENT_PATH = os.getcwd()
FOLDER = 'upscale_app'
IMAGE = 'lama_300px.png'
PATH_TO_IMAGE = os.path.join(CURRENT_PATH, FOLDER, IMAGE)


with open(PATH_TO_IMAGE, 'rb') as image:
    response = requests.post('http://127.0.0.1:5000/upscale', files={'image': image}).json()
    task_id = response['task_id']

    while True:
        time.sleep(1)
        response = requests.get(f'http://127.0.0.1:5000/tasks/{task_id}')
        status_code = response.status_code
        response = response.json()
        print(response)
        assert status_code == 200
        if response['status'] == 'SUCCESS':
            url = response['link']
            image = requests.get(url)
            status_code = image.status_code
            assert status_code == 200
            break
