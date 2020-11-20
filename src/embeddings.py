import abc

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

        return distances[:k]


class EuclideanMetric(EmbeddingMetric):
    def __init__(self, vectors, scaling_max=1.3, scaling_min=0):
        super(EuclideanMetric, self).__init__(vectors)
        self.scaling_max = scaling_max
        self.scaling_min = scaling_min

    def get_distance(self, first, second):
        emb_1 = self.vectors.query(first)
        emb_2 = self.vectors.query(second)

        value = np.linalg.norm(emb_1 - emb_2)
        return (((value - self.scaling_min) * (0 - 10)) / (
                self.scaling_max - self.scaling_min)) + 10


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


if __name__ == '__main__':
    simlex_data = load_simlex_data()

    dictionary = set()
    dictionary.update(simlex_data['word1'].unique())
    dictionary.update(simlex_data['word2'].unique())

    cosine_metric = CosineMetric(
        Magnitude('../data/nkjp+wiki-lemmas-restricted-300-skipg-ns.magnitude'))

    euklidean_metric = EuclideanMetric(
        Magnitude('../data/nkjp+wiki-lemmas-restricted-300-skipg-ns.magnitude'))

    anchor_word = 'kompania'
    k = 20

    k_nearest_euklidean = euklidean_metric.get_k_nearest(
        anchor_word, k, dictionary
    )

    k_nearest_cosine = cosine_metric.get_k_nearest(
        anchor_word, k, dictionary
    )

    print(f"{k} nearest words to {anchor_word} by euclidean metric")
    print(k_nearest_euklidean)
    print(f"{k} nearest words to {anchor_word} by cosine metric")
    print(k_nearest_cosine)
