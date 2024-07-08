import asyncio
import logging
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from utils.agent_utils import start_thread
from utils.graph_gen import process_openapi
from utils.openapi_utils import parse_spec

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = AsyncOpenAI()
asst_id = os.environ["OPENAI_PARROT_AGENT_ASST"]

test_spec = "test-openapi.json"
openapi_json = parse_spec(test_spec)

asset_nodes, graph = process_openapi(openapi=openapi_json)

logging.info(asset_nodes)
logging.info(graph)

user_query = "I want to create an evaluation dataset with 10 test cases about ohio."

thread_id = asyncio.run(start_thread(async_client=client, assets=asset_nodes, user_query=user_query))
logging.info(thread_id)
