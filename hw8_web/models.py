from mongoengine import Document, connect
from mongoengine.fields import StringField, ListField, ReferenceField

connect(host="mongodb://localhost:27017/hw_o8")


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author)
    quote = StringField()