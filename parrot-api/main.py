from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

load_dotenv()


@app.get("/")
def read_root():
    client = OpenAI()
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}