import os
import time
import pika
import json
import asyncio

from pika_client import PikaClient
from enums import Classifier


class RaisonText:
    def __init__(self) -> None:
        pass

    def evaluate_quality(self, text: str, classifier: Classifier = None) -> float:
        if classifier == Classifier.NaiveClassifier or classifier is None:
            if len(text) > 10:
                score = 1
            elif len(text) > 5:
                score = 0.5
            else:
                score = 0
        else:
            raise NotImplementedError
        return score


class ModelPikaClient(PikaClient):

    def __init__(self, publish_queue_name, consume_queue_name):
        self.publish_queue_name = publish_queue_name  # "raisontext_model"
        self.consume_queue_name = consume_queue_name  # "raisontext_answer"
        self.evaluator = RaisonText()

        self.connection = pika.BlockingConnection(
            pika.URLParameters("amqps://efiosdwv:5Mg1vBx3EbTu9RB4mRpj7xEOZh5XKXoz@cow.rmq2.cloudamqp.com/efiosdwv")
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=publish_queue_name, durable=True)
        self.consume_queue = self.channel.queue_declare(queue=consume_queue_name, durable=True)

        self.publish_callback_queue = self.publish_queue.method.queue
        self.consume_callback_queue = self.consume_queue.method.queue

        self.response = None

    def process_callable(self, message: dict):
        print(f"In model {message}")
        text = message['text']
        print(f"In model text: {text}")
        prediction = self.evaluator.evaluate_quality(text)

        self.send_message(
            {
                "answer": str(prediction)
            }
        )

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        await message.ack()
        body = message.body
        print('Received message')
        if body:
            self.process_callable(self, json.loads(body))


async def startup(pika_client):
    loop = asyncio.get_running_loop()
    task = loop.create_task(pika_client.consume(loop))
    await task


async def main():
    model_pika_client = ModelPikaClient(
        publish_queue_name="raisontext_answer",
        consume_queue_name="raisontext_model"
    )

    await startup(model_pika_client)


main()
while True:
    print("Model pika client")
    time.sleep(1)
