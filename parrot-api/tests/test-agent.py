import asyncio
import json
import logging
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from models.request_models import AgentKickoffRequest
from use_cases.agent_use_case import AgentUseCase

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = AsyncOpenAI()
asst_id = os.environ["OPENAI_PARROT_AGENT_ASST"]
BASE_URL = "https://api.egp.scale.com"
HEADERS = {"x-api-key": "c5ae00cd-6190-41cd-802e-b2d848b11fb8"}  # "x-selected-account-id": "6630377a5a7b09c735cfeebb"


async def main():
    file_path = "test-openapi.json"

    with open(file_path, 'r') as file:
        test_spec = json.load(file)

    user_query = "I want to create a question set with 10 questions about tennis. create the question set and questions. use the account id '6630377a5a7b09c735cfeebb'."

    request = AgentKickoffRequest(
        query=user_query,
        headers=HEADERS,
        openapi=test_spec,
        base_url=BASE_URL,
    )

    agent = AgentUseCase(async_client=client, asst_id=asst_id)

    async for value in agent.kickoff(params=request):
        print(value)


if __name__ == '__main__':
    asyncio.run(main())
