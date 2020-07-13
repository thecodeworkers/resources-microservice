from google.protobuf.json_format import MessageToDict
from mongoengine.queryset import NotUniqueError
from ..bootstrap import grpc_server, service_bus
from ...protos import CurrencyServicer, CurrencyMultipleResponse, CurrencyResponse, CurrencyTableResponse, Empty, add_CurrencyServicer_to_server
from ...utils import parser_all_object, parser_one_object, not_exist_code, exist_code, paginate
from ...models import Currency

class CurrencyService(CurrencyServicer):
    def __init__(self):
        self.__emit_currencies()

    def table(self, request, context):
        currency = Currency.objects
        response = paginate(currency, request.page)
        response = CurrencyTableResponse(**response)
        
        return response

    def get_all(self, request, context):
        currencies = self.__get_all_currencies()
        response = CurrencyMultipleResponse(currency=currencies)

        return response

    def get(self, request, context):
        try:
            currency = Currency.objects.get(id=request.id)
            currency = parser_one_object(currency)
            response = CurrencyResponse(currency=currency)

            return response

        except Currency.DoesNotExist as e:
            not_exist_code(context, e)

    def save(self, request, context):
        try:
            currency_object = MessageToDict(request)
            currency = Currency(**currency_object).save()
            currency = parser_one_object(currency)
            response = CurrencyResponse(currency=currency)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def update(self, request, context):
        try:
            currency_object = MessageToDict(request)
            currency = Currency.objects(id=currency_object['id'])

            if not currency: del currency_object['id']

            currency = Currency(**currency_object).save()
            currency = parser_one_object(currency)
            response = CurrencyResponse(currency=currency)
        
            return response

        except NotUniqueError as e:
            exist_code(context, e)
        
    def delete(self, request, context):
        try:
            currency = Currency.objects.get(id=request.id)
            currency = currency.delete()
            response = Empty()

            return response

        except Currency.DoesNotExist as e:
            not_exist_code(context, e)

    def __emit_currencies(self):
        service_bus.send('currencies', self.__get_all_currencies)

    def __get_all_currencies(self):
        return parser_all_object(Currency.objects.all())
        
def start_currency_service():
    add_CurrencyServicer_to_server(CurrencyService(), grpc_server)
