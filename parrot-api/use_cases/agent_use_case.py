from datetime import datetime
import json
import os
import logging
from typing import Annotated, Optional, Dict

import jsonref
from fastapi import Depends
from openai import AsyncOpenAI, BaseModel

from models.agent_models import AgentLog, AgentLogType
from models.request_models import AgentKickoffRequest
from tools.fetch_api_spec import fetch_api_spec
from tools.get_dependency_tree import get_dependency_tree
from tools.run_api_call import run_api_call
from utils.agent_utils import start_thread
from utils.graph_gen import process_openapi


def get_async_openai_client():
    return AsyncOpenAI()


def get_asst_id():
    return os.environ["OPENAI_PARROT_AGENT_ASST"]


class AgentUseCase:
    def __init__(self, async_client: AsyncOpenAI = Depends(get_async_openai_client), asst_id: str = Depends(get_asst_id)):
        self.async_client = async_client
        self.asst_id = asst_id

    async def kickoff(self, params: AgentKickoffRequest):
        user_query = params.query
        headers = params.headers
        base_url = params.base_url

        yield AgentLog(
            type=AgentLogType.INFO,
            message="Agent preprocessing...",
            metadata={}
        ).model_dump_json()

        start = datetime.now()

        json_str = json.dumps(params.openapi)
        openapi_json = jsonref.loads(json_str)

        asset_nodes, graph = process_openapi(openapi=openapi_json)

        logging.info(asset_nodes)
        logging.info(graph)

        thread = await start_thread(async_client=self.async_client, assets=asset_nodes, user_query=user_query)
        logging.info(f"Thread Started: {thread.id}")

        yield AgentLog(
            type=AgentLogType.INFO,
            message="Agent successfully started",
            metadata={}
        ).model_dump_json()

        run = await self.async_client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=self.asst_id,
            tool_choice="required"
        )

        while run.status == "requires_action":
            # Define the list to store tool outputs
            tool_outputs = []
            num_tools = len(run.required_action.submit_tool_outputs.tool_calls)
            logging.info(f"Number of tool calls: {num_tools}")

            if num_tools == 0:
                break

            # execute tool requests
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                logging.info(f"Tool called: {tool}")
                arguments = json.loads(tool.function.arguments)

                yield AgentLog(
                    type=AgentLogType.TOOL_IN,
                    message=f"Running tool: {tool.function.name}",
                    metadata=arguments
                ).model_dump_json()

                output = "Tool not found"
                if tool.function.name == "run_api_call":

                    api_out = run_api_call(
                        route=arguments['route'],
                        method=arguments['method'],
                        data=arguments.get("requestBody", None),
                        base_url=base_url,
                        headers=headers,
                    )

                    output = str(api_out)
                elif tool.function.name == "get_dependency_tree":

                    tree_out = get_dependency_tree(
                        resource_name=arguments["resource_name"],
                        graph=graph
                    )

                    output = tree_out
                elif tool.function.name == "fetch_api_spec":
                    api_info = fetch_api_spec(
                        resource_name=arguments["resource_name"],
                        assets=asset_nodes,
                        openapi=openapi_json,
                    )

                    output = api_info

                tool_output = {
                    "tool_call_id": tool.id,
                    "output": output
                }

                yield AgentLog(
                    type=AgentLogType.TOOL_OUT,
                    message=f"Tool complete: {tool.function.name}",
                    metadata=tool_output if tool.function.name not in {"fetch_api_spec"} else {}
                ).model_dump_json()

                tool_outputs.append(tool_output)

            # submit tool results
            if tool_outputs:
                try:
                    run = await self.async_client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    logging.info("Tool outputs submitted successfully.")
                except Exception as e:
                    logging.info(f"Failed to submit tool outputs: {e}")
            else:
                logging.info("No tool outputs to submit.")
                break

        if run.status == 'completed':
            messages = await self.async_client.beta.threads.messages.list(
                thread_id=thread.id
            )
            final_msg = messages.data[0].content[0].text.value
            logging.info(f"Final message {final_msg}")

            duration = datetime.now() - start
            minutes, seconds = divmod(duration.total_seconds(), 60)
            formatted_duration = f"{int(minutes)}:{int(seconds):02d}"

            yield AgentLog(
                type=AgentLogType.INFO,
                message=f"{final_msg}",
                terminal=True,
                metadata={
                    "time": formatted_duration
                }
            ).model_dump_json()
        else:
            logging.info(f"Failed with status: {run.status}")

        thread_messages = await self.async_client.beta.threads.messages.list(thread.id)
        logging.info(f"Complete Thread: {thread_messages.data}")

        run_steps = await self.async_client.beta.threads.runs.steps.list(
            thread_id=thread.id,
            run_id=run.id
        )
        logging.info(f"Run trace: {run_steps.data}")


DAgentUseCase = Annotated[AgentUseCase, Depends(AgentUseCase)]
