FROM python:3.10


WORKDIR /app

COPY . .

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN apt update && apt install libgl1-mesa-glx -y

CMD celery -A main.celery_ worker -c 2