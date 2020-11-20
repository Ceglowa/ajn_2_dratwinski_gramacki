import networkx as nx
import numpy as np

from wordnet_utils.graph_operations import create_undirected_graph


class WordNetSimilarities:

    def __init__(self, graph: nx.DiGraph):
        self.nodes_set = set([int(node) for node in graph.nodes])
        self.graph = graph
        self.undirected_graph = create_undirected_graph(graph)
        self.double_max_depth_of_taxonomy = 2 * nx.dag_longest_path_length(graph)

    def wu_palmer(self, first_node: int, second_node: int) -> float:
        if first_node in self.nodes_set and second_node in self.nodes_set:
            if first_node == second_node:
                return 1.0
            first_node_str = str(first_node)
            second_node_str = str(second_node)
            lowest_common_anc = nx.lowest_common_ancestor(self.graph,
                                                          first_node_str,
                                                          second_node_str)
            if lowest_common_anc is not None:
                all_ancestors = nx.algorithms.dag.ancestors(self.graph,
                                                            lowest_common_anc)
                if len(all_ancestors) == 0:
                    lca_depth = 2
                else:
                    lca_depth = min(
                        [nx.shortest_path_length(self.graph, anc, lowest_common_anc) for anc in all_ancestors
                         if self.graph.in_degree(anc) == 0]) + 2

                first_depth = nx.shortest_path_length(self.graph, lowest_common_anc, first_node_str) + lca_depth
                second_depth = nx.shortest_path_length(self.graph, lowest_common_anc, second_node_str) + lca_depth
                wu_palmer_value = (2 * lca_depth) / (first_depth + second_depth)

            else:
                all_ancestors_for_first = nx.algorithms.dag.ancestors(
                    self.graph,
                    first_node_str)
                if len(all_ancestors_for_first) == 0:
                    length_for_first = 2
                else:
                    length_for_first = min(
                        [nx.shortest_path_length(self.graph, anc, first_node_str) for anc in all_ancestors_for_first
                        if self.graph.in_degree(anc) == 0]) + 2

                all_ancestors_for_second = nx.algorithms.dag.ancestors(self.graph, second_node_str)
                if len(all_ancestors_for_second) == 0:
                    length_for_second = 2
                else:
                    length_for_second = min([nx.shortest_path_length(self.graph, anc, second_node_str)
                                             for anc in all_ancestors_for_second
                                             if self.graph.in_degree(anc) == 0]) + 2

                wu_palmer_value = 2 / (length_for_first + length_for_second)
            return wu_palmer_value
        else:
            return self.not_found_in_graph(first_node, second_node)

    def leacock_chodrow(self, first_node: int, second_node: int) -> float:
        if first_node in self.nodes_set and second_node in self.nodes_set:
            path_length_between_nodes = nx.shortest_path_length(
                self.undirected_graph, str(first_node), str(second_node))
            return -np.log10(
                path_length_between_nodes / self.double_max_depth_of_taxonomy)
        else:
            return self.not_found_in_graph(first_node, second_node)

    def not_found_in_graph(self, first_node: int, second_node: int):
        if first_node not in self.nodes_set and second_node not in self.nodes_set:
            print(
                f"{first_node} and {second_node} not found in the specified graph. Returning -1")
        if first_node not in self.nodes_set and second_node in self.nodes_set:
            print(
                f"{first_node} not found in the specified graph. Returning -1")
        if first_node in self.nodes_set and second_node not in self.nodes_set:
            print(
                f"{second_node} not found in the specified graph. Returning -1")
        return -1