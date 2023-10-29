import aiofiles
import pickle
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import FileResponse

import config


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ClassifyText(BaseModel):
    text: str = ""

@app.get("/")
async def home():
    return FileResponse('static/html/home.html')

@app.post("/classify")
async def classify(payload: ClassifyText = None):
    """
        Function for text classification
    """
    text = payload.text
    print(text)

    MODELS_DIR = config.REPO_ROOT / 'models'
    model_dir = MODELS_DIR / 'TfIdfLogReg_first silly baseline'
    model_name = '4a015324-601a-43d3-9df9-856323b97f0d.pkl'
    with open(model_dir / model_name, 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict(text)

    return {
        'result': prediction
    }
