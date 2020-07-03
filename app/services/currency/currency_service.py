from concurrent import futures
import time
import grpc
import sys
import os
from ...protos import CurrencyServicer, CurrencyMultipleResponse, add_CurrencyServicer_to_server
from ..bootstrap import server

class CurrencyService(CurrencyServicer):
    def getAll(self, request, context):
        response = CurrencyMultipleResponse(currency=[
            {
                'name': 'Bitcoin',
                'color': '#FFF',
                'type': 'CRYPTO',
                'symbol': 'BTC',
                'price': 9100,
                'active': True
            }
        ])

        return response

    def save(self, request, context):
        print('save')

if(__name__ == 'app.services.currency.currency_service'):
    add_CurrencyServicer_to_server(CurrencyService(), server)
