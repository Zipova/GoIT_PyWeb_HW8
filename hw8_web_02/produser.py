import pika
from faker import Faker


import json

from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')

fake = Faker()


def main():
    for i in range(5):
        Contact(fullname=fake.name(),
                email=fake.email()).save()

    contacts = Contact.objects()
    for contact in contacts:
        contact_id = str(contact.id)

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=contact_id,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % contact_id)
    connection.close()


if __name__ == '__main__':
    main()

