import aiofiles
import asyncio
import pickle
import os
from pathlib import Path
from typing import Dict

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import FileResponse
import pika

import config
from raisontext import RaisonText
from enums import Classifier
from pika_client import PikaClient


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
# url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
# print('Here I am')
url = "amqps://efiosdwv:5Mg1vBx3EbTu9RB4mRpj7xEOZh5XKXoz@cow.rmq2.cloudamqp.com/efiosdwv"
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel_send_request = connection.channel()  # start a channel
channel_send_request.queue_declare(queue="raisontext_model", durable=True)  # Declare a queue


def print_function(message: dict):
    print('Here we got incoming message %s', message)


pika_client = PikaClient(
    print_function,
    "raisontext_model",
    "raisontext_answer"
)


class ClassifyText(BaseModel):
    text: str = ""


async def start():
    print("Here")
    channel_get_answer = connection.channel()  # start a channel
    channel_get_answer.queue_declare(queue="raisontext_answer", durable=True)  # Declare a queue

    def callback(ch, method, properties, body):
        print("In callback")
        print("[x] Received " + str(body))

    channel_get_answer.basic_consume('raisontext_answer', callback, auto_ack=True)
    await channel_get_answer.start_consuming()
    print("Not here")


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(foo_app.pika_client.consume(loop))
    await task


@app.get("/")
async def home():
    return FileResponse('static/html/home.html')


@app.post("/classify")
async def classify(payload: ClassifyText = None) -> Dict[str, str]:
    """
        Function for text classification
    """
    text = payload.text
    print(text)

    if text:
        # evaluator = RaisonText()

        # MODELS_DIR = os.path.join(config.REPO_ROOT, 'models')
        # model_dir = MODELS_DIR / 'TfIdfLogReg_first silly baseline'
        # model_name = '4a015324-601a-43d3-9df9-856323b97f0d.pkl'
        # with open(model_dir / model_name, 'rb') as f:
        #     model = pickle.load(f)

        channel_send_request.basic_publish(
            exchange='',
            routing_key='raisontext_model',
            body=text
        )

        print(f"[x] Sent {text}")
        # connection.close()

        # prediction = evaluator.evaluate_quality(text, Classifier.NaiveClassifier)

        prediction = 0.5
        status = 'OK'
    else:
        prediction = None
        status = 'null'

    print(prediction)

    return {
        'status': status,
        'prediction': str(prediction)
    }

start()
