import aiofiles
import pickle
import os
from pathlib import Path

from typing import Dict

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import FileResponse

import config
from raisontext import RaisonText
from enums import Classifier


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
async def classify(payload: ClassifyText = None) -> Dict[str, str]:
    """
        Function for text classification
    """
    text = payload.text
    print(text)

    if text:
        evaluator = RaisonText()

        # MODELS_DIR = os.path.join(config.REPO_ROOT, 'models')
        # model_dir = MODELS_DIR / 'TfIdfLogReg_first silly baseline'
        # model_name = '4a015324-601a-43d3-9df9-856323b97f0d.pkl'
        # with open(model_dir / model_name, 'rb') as f:
        #     model = pickle.load(f)

        prediction = evaluator.evaluate_quality(text, Classifier.NaiveClassifier)
        status = 'OK'
    else:
        prediction = None
        status = 'null'

    print(prediction)

    return {
        'status': status,
        'prediction': str(prediction)
    }
