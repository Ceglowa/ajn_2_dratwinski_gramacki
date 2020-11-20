from networkx import MultiDiGraph, DiGraph, simple_cycles, Graph
from igraph import Graph


def get_graph_with_specified_relation(graph: MultiDiGraph, relation="hiperonimia") -> DiGraph:
    edges_with_hiperonimia = {(e[0], e[1]): e[2] for e in graph.edges if e[2].endswith(relation)}
    filtered_graph = DiGraph()
    filtered_graph.add_edges_from(edges_with_hiperonimia)
    return filtered_graph


def delete_two_cycles_from_hiperonimia_graph(graph: DiGraph) -> None:
    list_of_cycles_before_remove = list(simple_cycles(graph))
    print(f"Number of cycles before removal: {len(list_of_cycles_before_remove)}")
    graph.remove_edge('2355', '44782')
    graph.remove_edge('55305', '2367')
    list_of_cycles_before_remove = list(simple_cycles(graph))
    print(f"Number of cycles after removal: {len(list_of_cycles_before_remove)}")

def create_undirected_graph(graph: DiGraph) -> Graph:
    copied_directed = graph.copy()

    copied_directed.add_node("0")
    for node in copied_directed.nodes:
        if copied_directed.in_degree(node) == 0 and node != "0":
            copied_directed.add_edge("0", node)

    return Graph(copied_directed)
