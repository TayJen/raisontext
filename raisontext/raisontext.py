import os
import time

import pika

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


if __name__ == "__main__":
    evaluator = RaisonText()

    # url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    url = "amqps://efiosdwv:5Mg1vBx3EbTu9RB4mRpj7xEOZh5XKXoz@cow.rmq2.cloudamqp.com/efiosdwv"
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel_request = connection.channel()  # start a channel
    channel_request.queue_declare(queue='raisontext_model', durable=True)  # Declare a queue

    channel_answer = connection.channel()  # start a channel
    channel_answer.queue_declare(queue="raisontext_answer", durable=True)  # Declare a queue

    def callback(ch, method, properties, body):
        print("[x] Received " + str(body))
        answer = evaluator.evaluate_quality(body)

        channel_answer.basic_publish(
            exchange='',
            routing_key='raisontext_answer',
            body=str(answer)
        )

    channel_request.basic_consume('raisontext_model', callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel_request.start_consuming()
    connection.close()
