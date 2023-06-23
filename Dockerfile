FROM python:3.8

WORKDIR /chat

COPY . /chat

RUN apt-get update && apt-get install -y redis-server

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD redis-server --daemonize yes