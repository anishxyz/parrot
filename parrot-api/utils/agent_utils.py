import logging
from typing import List, Optional

from openai import AsyncOpenAI, OpenAI

from models.openapi_models import Resource


async def start_thread(
        assets: List[Resource],
        user_query: str,
        async_client: AsyncOpenAI,
):
    asset_names = [str(asset.name) for asset in assets]

    message = """You are going to assist a user with an API. The user's API has the following resources you can act on:
{}        

Your goal is to complete the users request below:          
{}
""".format('\n'.join(asset_names), user_query)

    message_thread = await async_client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": message
            },
        ]
    )

    logging.debug(message_thread)

    return message_thread
