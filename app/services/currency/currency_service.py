from ...protos import CurrencyServicer, CurrencyMultipleResponse, add_CurrencyServicer_to_server
from ..bootstrap import grpc_server
from ...models import Currency
from ...utils import parserAllObject

class CurrencyService(CurrencyServicer):
    def getAll(self, request, context):
        currencies = parserAllObject(Currency)
        response = CurrencyMultipleResponse(currency=currencies)

        return response

    def save(self, request, context):
        print('save')

def start_currency_service():
    add_CurrencyServicer_to_server(CurrencyService(), grpc_server)
