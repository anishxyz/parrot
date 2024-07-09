import logging
from typing import List

from models.openapi_models import Resource
from utils.openapi_utils import schema_to_string


def fetch_api_spec(resource_name: str, assets: List[Resource], openapi: dict):
    """
    Retrieves API specifications for a specified resource from a list of assets.

    Parameters:
    - resource_name (str): The name of the resource for which to fetch specifications.
    - assets (List[Resource]): A list of Resource objects that may contain relevant information.
    - openapi (dict): A dictionary containing the OpenAPI specifications.

    Returns:
    - dict: A dictionary containing the API specifications for the requested resource.

    Function Call:
    {
      "name": "fetch_api_spec",
      "description": "Retrieves API specifications for a specified resource from openapi",
      "parameters": {
        "type": "object",
        "properties": {
          "resource_name": {
            "type": "string",
            "description": "The name of the resource for which to fetch specifications."
          }
        },
        "required": [
          "resource_name",
        ]
      }
    }
    """

    resource = next((res for res in assets if res.name == resource_name), None)

    if not resource:
        return "resource does not exist"

    route = resource.route
    path_def = openapi['paths'][route]

    for method, details in path_def.items():
        if method in ["post"]:
            description = details.get("description")

            request_body_json = details.get("requestBody")
            schema = request_body_json['content']['application/json']['schema']
            schema_str = schema_to_string(schema)

            output_str = f"""Route: {method} '{route}'
Description:
{description}

The request body is summarized below, but the openapi requestBody schema will also be provided
{schema_str}

{schema}            
"""
            logging.info(output_str)
            return output_str

    return "Could not find openapi route"


