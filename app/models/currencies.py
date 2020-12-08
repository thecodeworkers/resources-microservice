from mongoengine import Document, StringField, BooleanField, DecimalField, ListField

CURRENCY_TYPE = ('FIAT', 'CRYPTO')

class Currencies(Document):
    name = StringField(min_length=2, max_length=100, required=True)
    color = StringField(min_length=2,max_length=7, required=True)
    gradients = ListField(StringField(min_length=2,max_length=7))
    active = BooleanField(default=True)
    type = StringField(min_length=2,max_length=10, required=True, choices=CURRENCY_TYPE)
    symbol = StringField(min_length=2,max_length=10, required=True, unique=True)
    price = DecimalField(min_length=2,min_value=0)
