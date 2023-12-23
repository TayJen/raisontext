import os
import time

import pika
import json

import config
from dev.train.tf_idf_log_reg import TfIdfLogReg
from dotenv import load_dotenv

import sys

sys.path.append('../../..')

if __name__ == "__main__":
    # evaluator = RaisonText()
    evaluator = TfIdfLogReg('Raisontext Logreg', wandb_log=False)
    weights_path = os.path.join(config.REPO_ROOT.parent, 'models', 'TfIdfLogReg_first silly baseline', '0c581279-c7e0-4317-9cb2-dbc0408d0b4f.pkl')
    evaluator.load(weights_path)
    assert False

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
