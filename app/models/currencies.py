from mongoengine import Document, StringField, BooleanField, DecimalField, ListField

CURRENCY_TYPE = ('FIAT', 'CRYPTO')

class Currencies(Document):
    name = StringField(max_length=100, required=True)
    color = StringField(max_length=7, required=True)
    gradients = ListField(StringField(max_length=7))
    active = BooleanField(default=True)
    type = StringField(max_length=10, required=True, choices=CURRENCY_TYPE)
    symbol = StringField(max_length=10, required=True, unique=True)
    price = DecimalField(min_value=0)
