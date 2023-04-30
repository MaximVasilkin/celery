FROM python:3.10


COPY ./app .

COPY ./requirements.txt .

EXPOSE 5000

RUN apt update && apt install libgl1-mesa-glx -y

RUN pip install -r requirements.txt

