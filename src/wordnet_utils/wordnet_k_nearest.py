from typing import Callable
import networkx as nx
from data_loader import load_simlex_data
from wordnet_utils.graph_operations import get_graph_with_specified_relation, \
    delete_two_cycles_from_hiperonimia_graph
from wordnet_utils.plwn_utils import load_plwn_data, get_synsets_from_lemma
from wordnet_utils.similarities import WordNetSimilarities
import os
import pickle as pkl

simlex_data = load_simlex_data("../../data/MSimLex999_Polish.txt")
graph = nx.read_graphml("../../data/graph.gml")
wn, synsets = load_plwn_data()

only_hiperonyms = get_graph_with_specified_relation(graph, "hiperonimia")
delete_two_cycles_from_hiperonimia_graph(only_hiperonyms)
wordnet_sim = WordNetSimilarities(only_hiperonyms)

def get_similarities(search_word: str, dictionary: set, similarity_measure: Callable):
    synset_for_search_word = get_synsets_from_lemma(synsets, search_word, use_dict=True)
    if synset_for_search_word is None:
        print(f"Word {search_word} not found in synsets. Returning empty list")
        return []
    else:
        distances = []
        for word in dictionary:
            synset_for_word = get_synsets_from_lemma(synsets, word, use_dict=True)
            if synset_for_word is not None:
                distances.append((word, similarity_measure(synset_for_search_word.id, synset_for_word.id)))
        distances.sort(key=lambda x: x[1], reverse=True)

        return distances

def get_similarities_for_both_measures(anchor_word: str):
    simlex_data = load_simlex_data()

    dictionary = set()
    dictionary.update(simlex_data['word1'].unique())
    dictionary.update(simlex_data['word2'].unique())

    similarites_wu_palmer = get_similarities(
        anchor_word, dictionary, wordnet_sim.wu_palmer
    )

    similarites_leacock_chodorow = get_similarities(
        anchor_word, dictionary, wordnet_sim.leacock_chodrow
    )
    return similarites_wu_palmer, similarites_leacock_chodorow


def run(word_to_be_analyzed: str, k: int):
    if os.path.isfile(f"../../results/wordnet_similarities/{word_to_be_analyzed}.pkl"):
        sims_file = open(f"../../results/wordnet_similarities/{word_to_be_analyzed}.pkl", 'rb')
        wp_sims, lc_sims = pkl.load(sims_file)
        sims_file.close()
    else:
        wp_sims, lc_sims = get_similarities_for_both_measures(word_to_be_analyzed)
        sims_file = open(f"../../results/wordnet_similarities/{word_to_be_analyzed}.pkl", 'wb')
        pkl.dump((wp_sims, lc_sims), sims_file)
        sims_file.close()
    print(f"{k} nearest words to {word_to_be_analyzed} by Wu-Palmer metric")
    print(wp_sims[:k])
    print(f"{k} nearest words to {word_to_be_analyzed} by Leacock-Chodorow metric")
    print(lc_sims[:k])

if __name__ == '__main__':
    run("głupi", 5)
