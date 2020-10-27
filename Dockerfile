FROM python:3.8-alpine

RUN mkdir /usr/app
WORKDIR /usr/app
COPY ./requirements.txt /usr/app
RUN apk add g++ linux-headers
COPY ./requirements.txt /tcw
VOLUME [ "/usr/app" ]
RUN pip install -r requirements.txt
CMD python run.py
