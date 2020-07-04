from ...protos import CurrencyServicer, CurrencyMultipleResponse, CurrencyResponse, Empty, add_CurrencyServicer_to_server
from ..bootstrap import grpc_server
from ...models import Currency, CURRENCY_TYPE
from ...utils import parser_all_object, parser_one_object
from google.protobuf.json_format import MessageToDict

class CurrencyService(CurrencyServicer):
    def getAll(self, request, context):
        currencies = parser_all_object(Currency.objects.all())
        response = CurrencyMultipleResponse(currency=currencies)

        return response

    def get(self, request, context):
        currency = Currency.objects.get(id=request.id)
        currency = parser_one_object(currency)
        response = CurrencyResponse(currency=currency)

        return response

    def save(self, request, context):
        currency_object = MessageToDict(request)
        currency = Currency(**currency_object).save()
        currency = parser_one_object(currency)
        response = CurrencyResponse(currency=currency)

        return response

    def update(self, request, context):
        currency_object = MessageToDict(request)
        currency = Currency.objects(id=currency_object['id'])

        if not currency: del currency_object['id']

        currency = Currency(**currency_object).save()
        currency = parser_one_object(currency)
        response = CurrencyResponse(currency=currency)
    
        return response

    def delete(self, request, context):
        currency = Currency.objects.get(id=request.id)
        currency = currency.delete()
        response = Empty()

        return response

def start_currency_service():
    add_CurrencyServicer_to_server(CurrencyService(), grpc_server)
