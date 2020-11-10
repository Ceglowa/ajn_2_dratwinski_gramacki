import pandas as pd
import os
import plwn

PATH_TO_DATA_FOLDER = "../data"

def load_simlex_data():
    simlex_data = pd.read_csv(PATH_TO_DATA_FOLDER + os.path.sep + "MSimLex999_Polish.txt", sep="\t", index_col=0,
                 names=["nr", "word1", "word2", "similarity","relatedness"])
    return simlex_data

def load_and_save_wordnet_to_graphml():
    wn = plwn.load_default()
    wn.to_graphml(PATH_TO_DATA_FOLDER + os.path.sep + "graph.gml")

if __name__ == '__main__':
    load_and_save_wordnet_to_graphml()