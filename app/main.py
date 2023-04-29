import os
import base64
import uuid
from flask import jsonify, request, send_file
from flask.views import MethodView
from celery.result import AsyncResult
from upscale_app import upscale
from celery import Celery
from flask import Flask
import redis
from config import PATH_TO_STORAGE, PATH_TO_MODEL


# redis storage

redis_dict = redis.Redis()


# flask app

app_name = 'my_app'
app = Flask(app_name)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


# Celery

celery_ = Celery(app_name, broker='redis://localhost:6379/2', backend='redis://localhost:6379/4')


class ContextTask(celery_.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery_.Task = ContextTask
upscaler_ = celery_.task(upscale.upscaler)


# views

def main_view():
    return jsonify({'message': 'Hi!'})


class TaskView(MethodView):
    def get(self, task_id):
        task = AsyncResult(task_id, app=celery_)
        status = task.status
        message = {'status': status}
        if status == 'SUCCESS':
            file_name = redis_dict.get(task_id)
            message.update({'link': f'{request.url_root}processed/{file_name.decode()}'})
        return jsonify(message)

    def post(self):
        image = self._get_image('image')
        image_str = base64.b64encode(image.read()).decode()
        upscaled_image_name = f'upscaled_{image.filename}'
        path = os.path.join(PATH_TO_STORAGE, upscaled_image_name)
        task = upscaler_.delay(image_str, path, PATH_TO_MODEL)
        redis_dict.mset({task.id: upscaled_image_name})
        return jsonify({'task_id': task.id})

    def _get_image(self, field):
        image = request.files.get(field)
        file_name = image.filename
        extension = file_name[file_name.rfind('.'):]
        file_name = uuid.uuid4()
        file_name = f'{file_name}{extension}'
        image.filename = file_name
        return image


class ImageView(MethodView):
    def get(self, file):
        return send_file(os.path.join(PATH_TO_STORAGE, file), mimetype='image/gif')


# urls

app.add_url_rule('/',
                 view_func=main_view,
                 methods=['GET'])

app.add_url_rule('/upscale',
                 view_func=TaskView.as_view('task_add'),
                 methods=['POST'])

app.add_url_rule('/tasks/<task_id>',
                 view_func=TaskView.as_view('task_get'),
                 methods=['GET'])

app.add_url_rule('/processed/<file>',
                 view_func=ImageView.as_view('image_get'),
                 methods=['GET'])


# Start project

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)
