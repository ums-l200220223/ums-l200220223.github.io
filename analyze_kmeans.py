from itertools import islice
import numpy as np

def top_words(num_clusters, clusters, mtx, columns):
    top = []
    for i in range(num_clusters):  # Loop over each cluster
        rows_in_cluster = np.where(clusters == i)[0]  # Get rows belonging to the current cluster
        word_freqs = mtx[rows_in_cluster].sum(axis=0).A[0]  # Sum word frequencies for the cluster
        ordered_freqs = np.argsort(word_freqs)  # Sort frequencies
        top_words = [
            (columns[idx], int(word_freqs[idx]))  # Get top words and their frequencies
            for idx in islice(reversed(ordered_freqs), 20)
        ]
        top.append(top_words)
    return top
