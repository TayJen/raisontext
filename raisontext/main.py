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


def print_function(message: dict):
    print(f'Here we got incoming message {message}')


pika_client = PikaClient(
    print_function,
    publish_queue_name="raisontext_model",
    consume_queue_name="raisontext_answer"
)


class ClassifyText(BaseModel):
    text: str = ""


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(pika_client.consume(loop))
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
        pika_client.send_message(
            {
                "text": text
            }
        )

        print(f"[x] Sent {text}")
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
