from mongoengine import Document, StringField, BooleanField, DecimalField

class Languages(Document):
    name = StringField(max_length=100, required=True)
    prefix = StringField(max_length=5, required=True)
    active = BooleanField(default=True)
