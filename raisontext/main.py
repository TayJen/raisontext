import asyncio
import pickle
import os
from pathlib import Path
from typing import Dict
from base64 import b64encode


from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import FileResponse
from dotenv import load_dotenv


from websocket_connection import ConnectionManager
from pika_client import PikaClient


app = FastAPI()
manager = ConnectionManager()
id_to_socket_dict = {}
load_dotenv()  # take environment variables from .env.

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def receive_prediction(message: dict):
    text = message['answer']
    id_ = message["id"]

    print(f'Here we got incoming message from {id_}: {text}')
    websocket = id_to_socket_dict.get(id_, None)
    if websocket is not None:
        await manager.send_personal_message(text, websocket)


pika_client = PikaClient(
    receive_prediction,
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


@app.websocket("/classify")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    id_ = b64encode(os.urandom(8)).decode('ascii')
    id_to_socket_dict[id_] = websocket
    try:
        while True:
            text = await websocket.receive_text()
            print(text)

            if text:
                pika_client.send_message(
                    {
                        "id": id_,
                        "text": text
                    }
                )

                print(f"[x] Sent {id_} with {text}")
            else:
                print("[x] Didn't send, no text :(")

    except WebSocketDisconnect:
        del id_to_socket_dict[id_]

        manager.disconnect(websocket)
        await manager.send_personal_message("Bye!!!", websocket)
