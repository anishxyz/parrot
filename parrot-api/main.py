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
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/query")
async def run(request: AgentKickoffRequest, agent: DAgentUseCase):

    async def event_stream():
        async for json_log in agent.kickoff(params=request):
            yield f"data: {json_log}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
