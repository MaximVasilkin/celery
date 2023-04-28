import requests
import time
#
response = requests.get('http://127.0.0.1:5000/tasks/b256bffe6-7a1a-4bc5-a056-e4dac67455e3').json()
print(response)
# with open(r'F:\HomeWorks\Celery\app\upscale_app\lama_300px.png', 'rb') as image:
#     response = requests.post('http://127.0.0.1:5000/upscale', files={'image': image}).json()
#     print(response)
    # task_id = res
    # for i in range(10):
    #     time.sleep(i)
    #     response = requests.get(f'127.0.0.1:5000/tasks/{task_id}').json()