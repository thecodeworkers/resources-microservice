from mongoengine import Document, StringField, BooleanField, DecimalField

TYPE = (
    ('FIAT', 'FIAT'),
    ('CRYPTO', 'CRYPTO')
)

class Currency(Document):
    name = StringField(max_length=100, required=True)
    color = StringField(max_length=7, required=True)
    active = BooleanField(default=True)
    type = StringField(max_length=10, required=True, choices=TYPE)
    symbol = StringField(max_length=10, required=True, unique=True)
    price = DecimalField(min_value=0)
