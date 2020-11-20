import numpy as np
from pymagnitude import Magnitude
from tqdm import tqdm

from data_loader import load_simlex_data


def get_euclidean_distance(first, second):
    emb_1 = vectors.query(first)
    emb_2 = vectors.query(second)

    value = np.linalg.norm(emb_1 - emb_2)
    return (((value - 0) * (0 - 10)) / (1.5 - 0)) + 10


def get_cosine_distance(first, second):
    emb_1 = vectors.query(first)
    emb_2 = vectors.query(second)

    emb_1 = emb_1 / np.linalg.norm(emb_1)
    emb_2 = emb_2 / np.linalg.norm(emb_2)

    value = np.dot(emb_1, emb_2)
    return (((value - -1) * (10 - 0)) / (1 - -1)) + 0


simlex_data = load_simlex_data()

vectors = Magnitude('../data/nkjp+wiki-lemmas-restricted-300-skipg-ns.magnitude')

out_of_vocab = set()
euclidean_dist = []
cosine_dist = []

for idx, row in tqdm(simlex_data.iterrows(), total=len(simlex_data)):
    if row['word1'] not in vectors:
        out_of_vocab.add(row['word1'])
    if row['word2'] not in vectors:
        out_of_vocab.add(row['word2'])

    euclidean_dist.append(get_euclidean_distance(row['word1'], row['word2']))
    cosine_dist.append(get_cosine_distance(row['word1'], row['word2']))

cosine_dist.append(get_cosine_distance('kot', 'kot'))
euclidean_dist.append(get_euclidean_distance('kot', 'kot'))

print(f"Out of vocab words: {out_of_vocab}")
print("Euclidean distance")
print(f'max: {max(euclidean_dist)}')
print(f'min: {min(euclidean_dist)}')
print(f'same: {euclidean_dist[-1]}')
print("Cosine distance")
print(f'max: {max(cosine_dist)}')
print(f'min: {min(cosine_dist)}')
print(f'same: {cosine_dist[-1]}')
