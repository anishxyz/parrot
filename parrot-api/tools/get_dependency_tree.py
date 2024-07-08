from networkx import DiGraph

from utils.graph_gen import get_node_from_graph, build_tree_for_node, tree_to_str


def get_dependency_tree(resource_name: str, graph: DiGraph):
    """
    :param resource_name: root of dependency graph
    :param graph: dependency digraph from api
    :return: tbd

    Function Call
    {
      "description": "Retrieves the dependency trees of a given API resource. Items shown with no following dependencies are leafs (you do not need to re-request a dependency tree for them)\nFor example if you have a graph RESOURCE_1 -> RESOURCE_2, you can assume RESOURCE_2 has no children (or it would be shown)",
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

    return tree_to_str(root_node)

