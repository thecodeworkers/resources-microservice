from google.protobuf.json_format import MessageToDict
from mongoengine.queryset import NotUniqueError
from ...protos import LanguageServicer, LanguageMultipleResponse, LanguageResponse, LanguageTableResponse, LanguageEmpty, add_LanguageServicer_to_server
from ...utils import parser_all_object, parser_one_object, not_exist_code, exist_code, paginate
from ..bootstrap import grpc_server
from ...models import Language

class LanguageService(LanguageServicer):
    def table(self, request, context):
        languages = Language.objects
        response = paginate(languages, request.page)
        response = LanguageTableResponse(**response)
        
        return response

    def get_all(self, request, context):
        languages = parser_all_object(Language.objects.all())
        response = LanguageMultipleResponse(language=languages)

        return response

    def get(self, request, context):
        try:
            language = Language.objects.get(id=request.id)
            language = parser_one_object(language)
            response = LanguageResponse(language=language)

            return response

        except Language.DoesNotExist as e:
            not_exist_code(context, e)

    def save(self, request, context):
        try:
            language_object = MessageToDict(request)
            language = Language(**language_object).save()
            language = parser_one_object(language)
            response = LanguageResponse(language=language)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def update(self, request, context):
        try:
            language_object = MessageToDict(request)
            language = Language.objects(id=language_object['id'])

            if not language: del language_object['id']

            language = Language(**language_object).save()
            language = parser_one_object(language)
            response = LanguageResponse(language=language)
        
            return response

        except NotUniqueError as e:
            exist_code(context, e)
        
    def delete(self, request, context):
        try:
            language = Language.objects.get(id=request.id)
            language = language.delete()
            response = LanguageEmpty()

            return response

        except Language.DoesNotExist as e:
            not_exist_code(context, e)

def start_language_service():
    add_LanguageServicer_to_server(LanguageService(), grpc_server)
