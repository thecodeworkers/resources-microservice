from ..models import Currencies
from ..settings import Database

def currency_seeder():
    database = Database()
    database.start_connection()

    datas = [
        {
            'name':"Dolar",
            'color': "#85bb65",
            'active': True,
            'type': 'FIAT',
            'symbol': '$',
            'price': 1
        },
        {
            'name':"Bitcoin",
            'color': "#ff8406",
            'active': True,
            'type': 'CRYPTO',
            'symbol': 'BTC',
            'price': 1
        },
        {
            'name':"Tether",
            'color': "#85bb65",
            'active': True,
            'type': 'CRYPTO',
            'symbol': 'USDT',
            'price': 1
        },
        {
            'name':"Ethereum",
            'color': "#393939",
            'active': True,
            'type': 'CRYPTO',
            'symbol': 'ETH',
            'price': 1
        },
        {
            'name':"Dash",
            'color': "#1872a4",
            'active': True,
            'type': 'CRYPTO',
            'symbol': 'DASH',
            'price': 1
        },
    ]

    for data in datas:
        exist_currency = Currencies.objects(symbol=data['symbol'])
        if not exist_currency: Currencies(**data).save()

    database.close_connection()