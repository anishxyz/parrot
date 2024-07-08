import asyncio
import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools.get_dependency_tree import get_dependency_tree
from tools.run_api_call import run_api_call
from utils.agent_utils import start_thread
from utils.graph_gen import process_openapi
from utils.openapi_utils import parse_spec

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI()
asst_id = os.environ["OPENAI_PARROT_AGENT_ASST"]
BASE_URL = "https://api.egp.scale.com"
HEADERS = {"x-api-key": "key"}

test_spec = "test-openapi.json"
openapi_json = parse_spec(test_spec)

asset_nodes, graph = process_openapi(openapi=openapi_json)

logging.info(asset_nodes)
logging.info(graph)

user_query = "I want to create an evaluation dataset with 10 test cases about ohio."

thread = start_thread(client=client, assets=asset_nodes, user_query=user_query)
logging.info(thread.id)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=asst_id,
    tool_choice="required"
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
else:
    print(run.status)

# Define the list to store tool outputs
tool_outputs = []

# Loop through each tool in the required action section
for tool in run.required_action.submit_tool_outputs.tool_calls:
    print(tool)
    arguments = json.loads(tool.function.arguments)
    if tool.function.name == "run_api_call":

        api_out = run_api_call(
            route=arguments['route'],
            method=arguments['method'],
            data=arguments.get("data", None),
            base_url=BASE_URL,
            headers=HEADERS
        )

        tool_outputs.append({
            "tool_call_id": tool.id,
            "output": str(api_out)
        })
    elif tool.function.name == "get_dependency_tree":

        tree_out = get_dependency_tree(
            resource_name=arguments["resource_name"],
            graph=graph
        )

        tool_outputs.append({
            "tool_call_id": tool.id,
            "output": tree_out
        })

# Submit all tool outputs at once after collecting them in a list
if tool_outputs:
    try:
        run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
        print("Tool outputs submitted successfully.")
    except Exception as e:
        print("Failed to submit tool outputs:", e)
else:
    print("No tool outputs to submit.")

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
else:
    print(run.status)
    print(run.required_action.submit_tool_outputs.tool_calls)

thread_messages = client.beta.threads.messages.list(thread.id)
print(thread_messages.data)