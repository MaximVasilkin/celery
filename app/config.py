import os


CURRENT_PATH = os.getcwd()
FOLDER = 'upscaled_files'
PATH_TO_STORAGE = os.path.join(CURRENT_PATH, FOLDER)

MODEL_FOLDER = 'upscale_app'
MODEL_NAME = 'EDSR_x2.pb'
PATH_TO_MODEL = os.path.join(CURRENT_PATH, MODEL_FOLDER, MODEL_NAME)
