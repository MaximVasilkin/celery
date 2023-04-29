import uuid
import os
from flask import jsonify, request, send_file
from flask.views import MethodView
from celery.result import AsyncResult
from upscale_app import upscale
from celery import Celery
from flask import Flask

import redis

redis_dict = redis.Redis()

app_name = 'my_app'
app = Flask(app_name)
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

celery_ = Celery(app_name, broker='redis://localhost:6379/2', backend='redis://localhost:6379/4')


class ContextTask(celery_.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery_.Task = ContextTask

upscaler_ = celery_.task(upscale.upscaler)

# error handlers

# @app.errorhandler(HttpError)
# def http_error_handler(error):
#     return __error_message(error.message, error.status_code)


# work with objects, validate, authenticate

# def validate(json, validate_model_class):
#     try:
#         model = validate_model_class(**json)
#         validated_json = model.dict(exclude_none=True)
#         if not validated_json:
#             raise HttpError(400, 'Validation error')
#         return validated_json
#     except ValidationError as error:
#         raise HttpError(400, error.errors())
#
#
# def __error_message(message, status_code):
#     response = jsonify({'message': message} | Status.error)
#     response.status_code = status_code
#     return response


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
        #return jsonify({'status': task.status, 'result': task.result})
        return jsonify(message)

    def post(self):
        image_name, image_path = self._save_image('image')
        upscaled_image_name = f'upscaled_{image_name}'
        task = upscaler_.delay(image_path, upscaled_image_name, r'F:\HomeWorks\Celery\app\upscale_app\EDSR_x2.pb')
        redis_dict.mset({task.id: upscaled_image_name})
        return jsonify({'task_id': task.id})

    def _save_image(self, field):
        image = request.files.get(field)
        file_name = image.filename
        extension = file_name[file_name.rfind('.'):]
        file_name = uuid.uuid4()
        file_name = f'{file_name}{extension}'
        path = os.path.join(UPLOAD_FOLDER, file_name)
        image.save(path)
        return file_name, path


class ImageView(MethodView):
    def get(self, file):
        return send_file(file, mimetype='image/gif')

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

