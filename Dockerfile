FROM python:3.8-alpine

RUN mkdir /project
WORKDIR /project
COPY ./requirements.txt /project
RUN apk add g++ linux-headers
RUN pip install -r requirements.txt
CMD python run.py

