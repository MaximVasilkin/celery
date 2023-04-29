import requests
import time


with open(r'F:\HomeWorks\Celery\app\upscale_app\lama_300px.png', 'rb') as image:
    response = requests.post('http://127.0.0.1:5000/upscale', files={'image': image}).json()
    task_id = response['task_id']
    for i in range(7):
        time.sleep(i)
        response = requests.get(f'http://127.0.0.1:5000/tasks/{task_id}').json()
        print(response)