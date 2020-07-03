from mongoengine import connect, disconnect
from .settings import DATABASE_NAME
from .models import Currency
import time
import sys
import os

from .services import server

class App():
  def __init__(self):
    print('Happy Coding')

    server.add_insecure_port('[::]:50051')
    server.start()
    print('Starting server. Listening on port 50051.')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
