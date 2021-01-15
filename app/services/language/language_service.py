from google.protobuf.json_format import MessageToDict
from mongoengine.queryset import NotUniqueError
from ...protos import LanguageServicer, LanguageMultipleResponse, LanguageResponse, LanguageTableResponse, LanguageEmpty, add_LanguageServicer_to_server
from ...utils import parser_all_object, parser_one_object, not_exist_code, exist_code, paginate, parser_context, pagination,default_paginate_schema
from ...utils.validate_session import is_auth
from ..bootstrap import grpc_server
from bson.objectid import ObjectId
from ...models import Languages

class LanguageService(LanguageServicer):
    def table(self, request, context):
        auth_token = parser_context(context, 'auth_token')
        is_auth(auth_token, '01_language_table')

        search = request.search
        
        pipeline = [
            {
                "$match": {
                    "$or": [
                        {"name": {"$regex": search, "$options": "i"}},
                        {"prefix": {"$regex": search, "$options": "i"}},
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "id": {"$first": {"$toString": "$_id"}},
                    "name": {"$first": "$name"},
                    "prefix": {"$first": "$prefix"},
                    "active": {"$first": "$active"},
                }
            },
            {
                "$project": {
                    "_id": 0
                }
            }
        ]

        pipeline = pipeline + pagination(request.page, request.per_page, {"name": 1})

        response = Languages.objects().aggregate(pipeline)

        response = LanguageTableResponse(**default_paginate_schema(response, request.page, request.per_page))

        return response

    def get_all(self, request, context):
        auth_token = parser_context(context, 'auth_token')
        is_auth(auth_token, '01_language_get_all')

        languages = parser_all_object(Languages.objects.all())
        response = LanguageMultipleResponse(language=languages)

        return response

    def get(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '01_language_get')

            language = Languages.objects.get(id=request.id)
            language = parser_one_object(language)
            response = LanguageResponse(language=language)

            return response

        except Languages.DoesNotExist as e:
            not_exist_code(context, e)

    def save(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '01_language_save')

            language_object = MessageToDict(request)
            language = Languages(**language_object).save()
            language = parser_one_object(language)
            response = LanguageResponse(language=language)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def update(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '01_language_update')

            language_object = MessageToDict(request)
            language = Languages.objects(id=language_object['id'])

            if not language: del language_object['id']

            language = Languages(**language_object).save()
            language = parser_one_object(language)
            response = LanguageResponse(language=language)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def delete(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '01_language_delete')

            language = Languages.objects.get(id=request.id)
            language = language.delete()
            response = LanguageEmpty()

            return response

        except Languages.DoesNotExist as e:
            not_exist_code(context, e)

def start_language_service():
    add_LanguageServicer_to_server(LanguageService(), grpc_server)
