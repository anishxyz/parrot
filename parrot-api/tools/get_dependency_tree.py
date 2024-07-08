import logging

from networkx import DiGraph

from utils.graph_gen import get_node_from_graph, build_tree_for_node, tree_to_str


def get_dependency_tree(resource_name: str, graph: DiGraph):
    """
    :param resource_name: root of dependency graph
    :param graph: dependency digraph from api
    :return: tbd

    Function Call
    {
      "description": "Retrieves the dependency trees of a given API resource. Items shown with no following dependencies are leaves (you do not need to re-request a dependency tree for them). For example, if you have a graph PARENT_RESOURCE -> CHILD_RESOURCE, you can assume CHILD_RESOURCE has no children. If a resource has NO dependencies, it will just be returned",
      "name": "get_dependency_tree",
      "parameters": {
        "type": "object",
        "properties": {
          "resource_name": {
            "description": "The name of the resource for which the dependency tree will be computed.",
            "type": "string"
          }
        },
        "required": [
          "resource_name"
        ]
      }
    }
    """

    node = get_node_from_graph(resource_name=resource_name, graph=graph)
    root_node = build_tree_for_node(graph=graph, node=node)

    tree_str = tree_to_str(root_node)
    logging.info(tree_str)

    return tree_str

