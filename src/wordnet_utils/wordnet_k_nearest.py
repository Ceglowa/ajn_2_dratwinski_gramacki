from typing import Callable
import networkx as nx
from data_loader import load_simlex_data
from wordnet_utils.graph_operations import get_graph_with_specified_relation, \
    delete_two_cycles_from_hiperonimia_graph
from wordnet_utils.plwn_utils import load_plwn_data, get_synsets_from_lemma
from wordnet_utils.similarities import WordNetSimilarities
import os
import numpy as np
import pickle as pkl



def get_similarities(search_word: str, dictionary: set, similarity_measure: Callable):
    wn, synsets = load_plwn_data()
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
    graph = nx.read_graphml("../../data/graph.gml")

    only_hiperonyms = get_graph_with_specified_relation(graph, "hiperonimia")
    delete_two_cycles_from_hiperonimia_graph(only_hiperonyms)
    wordnet_sim = WordNetSimilarities(only_hiperonyms)

    simlex_data = load_simlex_data("../../data/MSimLex999_Polish.txt")

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
    while wp_sims[0][1]==1.0:
        wp_sims = wp_sims[1:]
    while lc_sims[0][1]==np.inf:
        lc_sims = lc_sims[1:]
    # print(f"{k} nearest words to {word_to_be_analyzed} by Wu-Palmer metric")
    # print(wp_sims[:k])
    # print(f"{k} nearest words to {word_to_be_analyzed} by Leacock-Chodorow metric")
    # print(lc_sims[:k])
    return wp_sims[:k], lc_sims[:k]

def print_results(wu_palms, leacocks):
    for w in wu_palms:
        print(f"{w[0]} - {round(w[1],4)} <br/> ",end="")
    print(" | ", end="")
    for l in leacocks:
        print(f"{l[0]} - {round(l[1],4)} <br/> ", end="")
    print()
    print()

if __name__ == '__main__':

    wp, lc = run("balkon", 10)
    print_results(wp,lc)
    wp, lc = run("drewno", 10)
    print_results(wp,lc)
    wp, lc = run("długopis", 10)
    print_results(wp,lc)
    wp, lc = run("ekran", 10)
    print_results(wp,lc)
    wp, lc = run("grzejnik", 10)
    print_results(wp,lc)
    wp, lc = run("głupi", 10)
    print_results(wp,lc)
    wp, lc = run("kapusta", 10)
    print_results(wp,lc)
    wp, lc = run("kot", 10)
    print_results(wp,lc)
    wp, lc = run("książka", 10)
    print_results(wp,lc)
    wp, lc = run("rower", 10)
    print_results(wp,lc)
    wp, lc = run("tapeta", 10)
    print_results(wp,lc)
    wp, lc = run("wycieczka", 10)
    print_results(wp,lc)
    wp, lc = run("zamek", 10)
    print_results(wp,lc)
    wp, lc = run("żniwa", 10)
    print_results(wp,lc)
