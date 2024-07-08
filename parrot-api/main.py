import os
from fastapi import FastAPI

from typing import Union

from dotenv import load_dotenv
import logging
from openai import AsyncOpenAI

app = FastAPI()

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test")
def test():

    return {"item_id": "asst_id"}


@app.post("/run")
def run():
    client = AsyncOpenAI()

    asst_id = os.environ["OPENAI_PARROT_AGENT_ASST"]

    return {"Hello": "World"}
