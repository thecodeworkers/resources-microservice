FROM python:3.8-alpine

RUN mkdir /tcw
WORKDIR /tcw
RUN apk add g++ linux-headers
COPY ./requirements.txt /tcw
VOLUME [ "/tcw" ]
RUN pip install -r requirements.txt
CMD python run.py
