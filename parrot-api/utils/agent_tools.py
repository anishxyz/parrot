from typing import List, Optional
import httpx


def run_api_call(route: str, method: str, base_url: str, headers: Optional[dict], data: Optional[dict] = None) -> dict:
    """
    Executes an HTTP request to a specified API endpoint.

    Parameters:
    - route (str): The API route or endpoint. Leading slashes are removed if present.
    - method (str): The HTTP method to be used for the request. Supported methods are 'GET', 'POST',
      'PATCH', and 'DELETE'.
    - base_url (str): The base URL of the API without a trailing slash.
    - headers (Optional[dict]): The headers to be included in the HTTP request.
    - data (Optional[dict]): The JSON payload for methods that send data; defaults to None if not provided.

    Returns:
    - dict: A dictionary containing the API's JSON response or an error message with the status code.

    Function Call:
    {
      "name": "run_api_call",
      "description": "Executes an HTTP request to a specified API endpoint supporting multiple methods. Assume BASE_URL and headers are handled",
      "parameters": {
        "type": "object",
        "properties": {
          "route": {
            "type": "string",
            "description": "The API route or endpoint. Leading slashes are removed if present."
          },
          "method": {
            "type": "string",
            "enum": [
              "GET",
              "POST",
              "PATCH",
              "DELETE"
            ],
            "description": "The HTTP method to be used for the request. Supported methods are GET, POST, PATCH, and DELETE."
          },
          "data": {
            "type": "object",
            "description": "The JSON payload for methods that send data. It is optional and defaults to None if not provided.",
            "nullable": true
          }
        },
        "required": [
          "route",
          "method"
        ]
      }
    }
    """

    url = f"{base_url}/{route.strip('/')}"
    with httpx.Client(headers=headers) as client:
        if method.upper() == 'POST':
            response = client.post(url, json=data)
        elif method.upper() == 'GET':
            response = client.get(url)
        elif method == 'PATCH':
            response = client.patch(url, json=data)
        elif method == 'DELETE':
            response = client.delete(url)
        else:
            return {"error": f"Unsupported method: {method}"}

        if response.is_success:
            return response.json()
        else:
            return {'status_code': response.status_code, 'detail': response.text}


def get_dependency_trees(resource_name: str, graph):
    # generate dependency tree



    pass


def get_routes_for_asset():
    pass
