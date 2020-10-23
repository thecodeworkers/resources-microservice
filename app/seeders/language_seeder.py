from ..models import Languages
from ..settings import Database

def language_seeder():
    database = Database()
    database.start_connection()

    datas = [
        {
            'name':"Espanol",
            'prefix': "es",
            'active': True
        },
        {
            'name':"English",
            'prefix': "en",
            'active': True
        }
    ]

    for data in datas:
        exist_language = Languages.objects(prefix=data['prefix'])
        if not exist_language: Languages(**data).save()
    
    database.close_connection()