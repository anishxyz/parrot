from typing import List, Dict, Optional, Tuple

import networkx as nx
import requests
from anytree import Node, RenderTree
from networkx import DiGraph

from utils.openapi_utils import standardize_asset_name, get_last_route_segment, last_part_has_id, resolve_schema_ref
from models.openapi_models import Resource
import logging


def organize_resources(spec) -> List[Resource]:
    node_registry: Dict[str, Resource] = {}

    get_assets = set()
    dependent_assets = set()
    all_tags = set()

    for path, methods in spec['paths'].items():
        if last_part_has_id(path):
            continue

        for method, details in methods.items():
            if method in ["get"]:
                get_assets.add(standardize_asset_name(get_last_route_segment(path)))

            if method not in ["post"] or last_part_has_id(path):  # maybe add `patch`
                continue

            tags = details.get("tags")

            dependents = set()
            inputs = set()

            bad_ids = ["account_id", "x-selected-account-id"]

            def handle_properties(_properties):
                for _input in _properties:
                    handle_input(_input)

            def handle_input(_input):
                if "id" in _input and _input not in bad_ids:
                    dependents.add(standardize_asset_name(_input))

                inputs.add(_input)

            # get ids from request body
            body = details.get("requestBody")
            if body:
                try:
                    content = details["requestBody"]["content"]
                    pointer = content.get("application/json", None)
                    if not pointer:
                        pointer = content["multipart/form-data"]
                    ref = pointer["schema"]
                    request_body_schema = resolve_schema_ref(spec, ref)

                    # properties
                    properties = request_body_schema.get("properties", None)
                    if properties:
                        handle_properties(properties)

                    # nestings
                    nested_patterns = ["allOf", "oneOf"]
                    for pat in nested_patterns:
                        if pat in request_body_schema:
                            for prop in request_body_schema[pat]:
                                if prop.get("properties", None):
                                    handle_properties(prop["properties"])

                except Exception as e:
                    logging.error(f"Error parsing request body {path} {e}")

            # get ids from parameters
            params = details.get("parameters")

            if params:
                try:
                    for param in params:
                        if param.get("name", None):
                            name = param["name"]
                            handle_input(name)

                except Exception as e:
                    logging.error(f"Error parsing parameters {path} {e}")

            # get ids from response
            # responses = details.get("responses")
            #
            # if responses:
            #     try:
            #         success_ref = responses["200"]["content"]["application/json"]["schema"]
            #         success_resp_schema = resolve_schema_ref(spec, success_ref)
            #
            #         properties = success_resp_schema.get("properties", None)
            #         if properties:
            #             handle_properties(properties)
            #
            #     except Exception as e:
            #         print(f"Error parsing responses {path}", e)

            dependent_assets.update(dependents)

            _tag = tags[0] if tags and len(tags) > 0 else None
            all_tags.add(standardize_asset_name(_tag))

            curr_asset = standardize_asset_name(get_last_route_segment(path))
            new_node = Resource(
                name=curr_asset,
                dependents=list(dependents),
                inputs=list(inputs),
                route=path,
                method=method,
                tag=_tag,
            )

            if curr_asset not in node_registry:
                node_registry[curr_asset] = new_node
            elif len(node_registry[curr_asset].dependents) < len(dependents):
                node_registry[curr_asset] = new_node

    logging.debug(dependent_assets)
    logging.debug(get_assets)
    logging.debug(all_tags)
    nodes = list(node_registry.values())
    real_nodes = []
    for node in nodes:
        curr_asset = node.name
        if curr_asset in get_assets or curr_asset in dependent_assets or curr_asset in all_tags:
            real_nodes.append(node)
        else:
            logging.debug(f"Removing {node.name}")

    return real_nodes


def build_dependency_tree(nodes: List[Resource]):
    graph = nx.DiGraph()

    for graph_node in nodes:
        graph.add_node(graph_node.name)

    # edges based on dependencies
    for graph_node in nodes:
        for dependent_asset in graph_node.dependents:
            graph.add_edge(dependent_asset, graph_node.name)
        logging.debug("-" * 50)
        logging.debug(graph_node.name)
        logging.debug(f"Children: {graph_node.dependents}")

    return graph


def process_openapi(openapi: Optional[dict] = None, openapi_url: Optional[str] = None) -> Tuple[List[Resource], DiGraph]:
    if not openapi_url and not openapi:
        raise ValueError("no api spec provided")
    if openapi_url and openapi:
        raise ValueError("provide an openapi spec OR openapi_url")
    if openapi_url:
        response = requests.get(openapi_url)
        response.raise_for_status()
        openapi = response.json()

    asset_nodes = organize_resources(openapi)
    graph = build_dependency_tree(asset_nodes)

    return asset_nodes, graph


# DiGraph - networkx nodes
def get_sink_nodes(graph):
    sink_nodes = [node for node in graph.nodes() if graph.out_degree(node) == 0]
    return sink_nodes


def build_tree_for_node(graph: DiGraph, node):  # networkx node
    nodes_dict = {}

    root = Node(node)
    nodes_dict[node] = root

    # dfs
    stack = [node]
    visited = set()

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for pred in graph.predecessors(node):
                if pred not in nodes_dict:
                    nodes_dict[pred] = Node(pred, parent=nodes_dict[node])
                else:
                    nodes_dict[pred].parent = nodes_dict[node]
                stack.append(pred)
    return root


def tree_to_str(root: Node) -> str:
    tree_str = f"Tree for {root.name}:\n"
    for pre, _, node in RenderTree(root):
        tree_str += "%s%s\n" % (pre, node.name)
    return tree_str
