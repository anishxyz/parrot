import json
import os
from fastapi import FastAPI

from typing import Union

from dotenv import load_dotenv
import logging
from openai import AsyncOpenAI
from starlette.responses import StreamingResponse

from models.request_models import AgentKickoffRequest
from use_cases.agent_use_case import DAgentUseCase

app = FastAPI()

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test")
def test():

    return {"item_id": "asst_id"}


@app.post("/query")
async def run(request: AgentKickoffRequest, agent: DAgentUseCase):

    async def event_stream():
        async for json_log in agent.kickoff(params=request):
            yield json_log + '\n'

    return StreamingResponse(event_stream(), media_type="application/x-ndjson")
