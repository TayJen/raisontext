import os
import time

import pika
import json

from enums import Classifier
from dotenv import load_dotenv


class RaisonText:
    def __init__(self) -> None:
        pass

    def evaluate_quality(self, text: str, classifier: Classifier = None) -> float:
        if classifier == Classifier.NaiveClassifier or classifier is None:
            time.sleep(5)
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
    load_dotenv()

    url = os.environ.get("RABBIT_MQ_URL")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel_request = connection.channel()  # start a channel
    channel_request.queue_declare(queue='raisontext_model', durable=True)  # Declare a queue

    channel_answer = connection.channel()  # start a channel
    channel_answer.queue_declare(queue="raisontext_answer", durable=True)  # Declare a queue

    def callback(ch, method, properties, body):
        dict_message = json.loads(body)
        id_ = dict_message['id']
        text = dict_message['text']
        print(f"[x] Received {id_} with {text}")

        answer = evaluator.evaluate_quality(text)
        answer_dict = {
            "id": id_,
            "answer": str(answer)
        }

        channel_answer.basic_publish(
            exchange='',
            routing_key='raisontext_answer',
            body=json.dumps(answer_dict)
        )

    channel_request.basic_consume('raisontext_model', callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel_request.start_consuming()
    connection.close()
