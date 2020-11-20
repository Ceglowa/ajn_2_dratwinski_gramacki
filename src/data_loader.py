import pandas as pd
import os
import plwn

PATH_TO_DATA_FOLDER = "../../data"

def load_simlex_data(path_to_simlex_data: str):
    simlex_data = pd.read_csv(path_to_simlex_data, sep="\t", index_col=0,
                 names=["nr", "word1", "word2", "similarity","relatedness"])
    return simlex_data

def load_and_save_wordnet_to_graphml(path_to_graphml: str):
    wn = plwn.load_default()
    wn.to_graphml(path_to_graphml)

if __name__ == '__main__':
    load_and_save_wordnet_to_graphml("../data/graph.gml")