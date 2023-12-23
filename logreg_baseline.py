import os
import sys
import time
import pickle
import json

import pika
import sklearn
from dotenv import load_dotenv


if __name__ == "__main__":
    evaluator = pickle.load(open("./models/TfIdfLogReg_first silly baseline/0c581279-c7e0-4317-9cb2-dbc0408d0b4f.pkl", 'rb'))
    print("Model is loaded")

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

        answer = evaluator.predict([text])
        answer_dict = {
            "id": id_,
            "answer": str(round(answer[0], 3))
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
