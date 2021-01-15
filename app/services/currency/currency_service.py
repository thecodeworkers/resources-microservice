from google.protobuf.json_format import MessageToDict
from mongoengine.queryset import NotUniqueError
from ...utils.validate_session import is_auth
from ...models import Currencies
from ...protos import *
from ...utils import *
from bson.objectid import ObjectId
from ..bootstrap import grpc_server

class CurrencyService(CurrencyServicer):
    def table(self, request, context):

        auth_token = parser_context(context, 'auth_token')
        is_auth(auth_token, '01_currency_table')

        search = request.search
        
        pipeline = [
            {
                "$match": {
                    "$or": [
                        {"name": {"$regex": search, "$options": "i"}},
                        {"color": {"$regex": search, "$options": "i"}},
                        {"type": {"$regex": search, "$options": "i"}},
                        {"symbol": {"$regex": search, "$options": "i"}},
                        {"price": {"$regex": search, "$options": "i"}},
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "id": {"$first": {"$toString": "$_id"}},
                    "name": {"$first": "$name"},
                    "color": {"$first": "$color"},
                    "gradients": {"$first": "$gradients"},
                    "active": {"$first": "$active"},
                    "type": {"$first": "$type"},
                    "symbol": {"$first": "$symbol"},
                    "price": {"$first": "$price"},
                }
            },
            {
                "$project": {
                    "_id": 0
                }
            }
        ]

        pipeline = pipeline + pagination(request.page, request.per_page, {"name": 1})

        response = Currencies.objects().aggregate(pipeline)

        response = CurrencyTableResponse(**default_paginate_schema(response, request.page, request.per_page))
    
        return response

    def get_all(self, request, context):
        auth_token = parser_context(context, 'auth_token')
        is_auth(auth_token, '01_currency_get_all')

        currencies = parser_all_object(Currencies.objects.all())
        response = CurrencyMultipleResponse(currency=currencies)

        return response

    def get(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '01_currency_get')

            currency = Currencies.objects.get(id=request.id)
            currency = parser_one_object(currency)
            response = CurrencyResponse(currency=currency)

            return response

        except Currencies.DoesNotExist as e:
            not_exist_code(context, e)

    def save(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '01_currency_save')

            currency_object = MessageToDict(request)
            currency = Currencies(**currency_object).save()
            currency = parser_one_object(currency)
            response = CurrencyResponse(currency=currency)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def update(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '01_currency_update')

            currency_object = MessageToDict(request)
            currency = Currencies.objects(id=currency_object['id'])

            if not currency: del currency_object['id']

            currency = Currencies(**currency_object).save()
            currency = parser_one_object(currency)
            response = CurrencyResponse(currency=currency)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def delete(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '01_currency_delete')

            currency = Currencies.objects.get(id=request.id)
            currency = currency.delete()
            response = CurrencyEmpty()

            return response

        except Currencies.DoesNotExist as e:
            not_exist_code(context, e)

def start_currency_service():
    add_CurrencyServicer_to_server(CurrencyService(), grpc_server)
