from flask import Flask
from celery import Celery
from upscale_app import upscale


app_name = 'my_app'
app = Flask(app_name)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


# Celery

celery_ = Celery(app_name, broker='redis://redis:6379/2', backend='redis://redis:6379/4')


class ContextTask(celery_.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery_.Task = ContextTask
upscaler_ = celery_.task(upscale.upscaler)
