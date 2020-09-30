from google.protobuf.json_format import MessageToDict
from mongoengine.queryset import NotUniqueError
from ...protos import LanguageServicer, LanguageMultipleResponse, LanguageResponse, LanguageTableResponse, LanguageEmpty, add_LanguageServicer_to_server
from ...utils import parser_all_object, parser_one_object, not_exist_code, exist_code, paginate
from ...utils.validate_session import is_auth
from ..bootstrap import grpc_server
from ...models import Languages

class LanguageService(LanguageServicer):
    def table(self, request, context):
        metadata = dict(context.invocation_metadata())
        is_auth(metadata['auth_token'], '01_language_table')
        languages = Languages.objects
        response = paginate(languages, request.page)
        response = LanguageTableResponse(**response)
        
        return response

    def get_all(self, request, context):
        metadata = dict(context.invocation_metadata())
        is_auth(metadata['auth_token'], '01_language_get_all')
        languages = parser_all_object(Languages.objects.all())
        response = LanguageMultipleResponse(language=languages)

        return response

    def get(self, request, context):
        try:
            metadata = dict(context.invocation_metadata())
            is_auth(metadata['auth_token'], '01_language_get')
            language = Languages.objects.get(id=request.id)
            language = parser_one_object(language)
            response = LanguageResponse(language=language)

            return response

        except Languages.DoesNotExist as e:
            not_exist_code(context, e)

    def save(self, request, context):
        try:
            metadata = dict(context.invocation_metadata())
            is_auth(metadata['auth_token'], '01_language_save')
            language_object = MessageToDict(request)
            language = Languages(**language_object).save()
            language = parser_one_object(language)
            response = LanguageResponse(language=language)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def update(self, request, context):
        try:
            metadata = dict(context.invocation_metadata())
            is_auth(metadata['auth_token'], '01_language_update')
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
            metadata = dict(context.invocation_metadata())
            is_auth(metadata['auth_token'], '01_language_delete')
            language = Languages.objects.get(id=request.id)
            language = language.delete()
            response = LanguageEmpty()

            return response

        except Languages.DoesNotExist as e:
            not_exist_code(context, e)

def start_language_service():
    add_LanguageServicer_to_server(LanguageService(), grpc_server)
