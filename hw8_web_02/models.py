from mongoengine import Document, connect
from mongoengine.fields import StringField, BooleanField

connect(host="mongodb://localhost:27017/hw_o8")


class Contact(Document):
    fullname = StringField()
    email = StringField()
    message_send = BooleanField(default=False)
