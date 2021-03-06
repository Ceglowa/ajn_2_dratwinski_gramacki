import abc
from typing import Union

import numpy as np
from pymagnitude import Magnitude
from tqdm import tqdm

from data_loader import load_simlex_data


class EmbeddingMetric(abc.ABC):
    def __init__(self, vectors):
        self.vectors = vectors

    @abc.abstractmethod
    def get_distance(self, first, second):
        pass

    def get_k_nearest(self, anchor, k, dictionary):
        if k > len(dictionary):
            raise ValueError

        distances = [
            (word, self.get_distance(anchor, word))
            for word in dictionary
        ]

        distances.sort(key=lambda x: x[1], reverse=True)

        return distances[1:k + 1]


class EuclideanMetric(EmbeddingMetric):
    def __init__(self, vectors):
        super(EuclideanMetric, self).__init__(vectors)
        self.epsilon = 10e-8

    def get_distance(self, first, second):
        emb_1 = self.vectors.query(first)
        emb_2 = self.vectors.query(second)

        value = np.linalg.norm(emb_1 - emb_2)
        return 1.5 - value


class CosineMetric(EmbeddingMetric):
    def __init__(self, vectors):
        super(CosineMetric, self).__init__(vectors)

    def get_distance(self, first, second):
        emb_1 = self.vectors.query(first)
        emb_2 = self.vectors.query(second)

        emb_1 = emb_1 / np.linalg.norm(emb_1)
        emb_2 = emb_2 / np.linalg.norm(emb_2)

        value = np.dot(emb_1, emb_2)
        return (((value - -1) * (10 - 0)) / (1 - -1)) + 0


def get_simlex_and_metrics():
    simlex_data = load_simlex_data('../data/MSimLex999_Polish.txt')
    euklidean_metric = EuclideanMetric(
        Magnitude('../data/nkjp+wiki-lemmas-restricted-300-skipg-ns.magnitude'))
    cosine_metric = CosineMetric(
        Magnitude('../data/nkjp+wiki-lemmas-restricted-300-skipg-ns.magnitude'))
    return simlex_data, euklidean_metric, cosine_metric


def prepare_for_report_tab(k_nearest):
    res = ""

    for word, distance in k_nearest:
        res = f'{res} </br> {word} - {distance:.4f} '

    print(res)


def test_k_nearest(k: int, anchor_word: str):
    simlex_data, euklidean_metric, cosine_metric = get_simlex_and_metrics()

    dictionary = set()
    dictionary.update(simlex_data['word1'].unique())
    dictionary.update(simlex_data['word2'].unique())

    k_nearest_euklidean = euklidean_metric.get_k_nearest(
        anchor_word, k, dictionary
    )

    k_nearest_cosine = cosine_metric.get_k_nearest(
        anchor_word, k, dictionary
    )

    print(f"{k} nearest words to {anchor_word} by euclidean metric")
    # print(k_nearest_euklidean)
    prepare_for_report_tab(k_nearest_euklidean)
    print(f"{k} nearest words to {anchor_word} by cosine metric")
    # print(k_nearest_cosine)
    prepare_for_report_tab(k_nearest_cosine)


def test_on_simlex(filename: Union[str, None] = None):
    simlex_data, euklidean_metric, cosine_metric = get_simlex_and_metrics()

    euclidean = []
    cosine = []

    for _, row in tqdm(simlex_data.iterrows(), total=len(simlex_data)):
        word1 = row['word1']
        word2 = row['word2']

        euclidean.append(euklidean_metric.get_distance(word1, word2))
        cosine.append(cosine_metric.get_distance(word1, word2))

    simlex_data['euclidean_metric'] = euclidean
    simlex_data['cosine_metric'] = cosine

    print(simlex_data)

    if filename is not None:
        simlex_data.to_csv(filename)


if __name__ == '__main__':
    words = ['drewno', 'głupi', 'kot', 'książka', 'rower']

    for word in words:
        test_k_nearest(10, word)
    # test_on_simlex('../results/emneddings_results.csv')
