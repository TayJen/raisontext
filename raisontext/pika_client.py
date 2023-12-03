import os
import uuid
import pika
from aio_pika import connect_robust
import json


class PikaClient:
    def __init__(self, process_callable, publish_queue_name, consume_queue_name):
        self.publish_queue_name = publish_queue_name
        self.consume_queue_name = consume_queue_name

        self.connection = pika.BlockingConnection(
            pika.URLParameters(os.environ.get("RABBIT_MQ_URL"))
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=publish_queue_name, durable=True)
        self.consume_queue = self.channel.queue_declare(queue=consume_queue_name, durable=True)

        self.publish_callback_queue = self.publish_queue.method.queue
        self.consume_callback_queue = self.consume_queue.method.queue

        self.response = None
        self.process_callable = process_callable

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        connection = await connect_robust(
            os.environ.get("RABBIT_MQ_URL"),
            loop=loop
        )

        channel = await connection.channel()
        queue = await channel.declare_queue(self.consume_queue_name, durable=True)
        await queue.consume(self.process_incoming_message, no_ack=False)
        return connection

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        await message.ack()
        body = message.body
        print('Received message')
        if body:
            await self.process_callable(json.loads(body))

    def send_message(self, message: dict):
        """Method to publish message to RabbitMQ"""
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.publish_callback_queue,
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )
