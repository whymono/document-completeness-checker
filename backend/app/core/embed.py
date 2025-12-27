from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# using the model 'all-MiniLM-L6-v2' for embedding
# having the threshold as 0.4
model = SentenceTransformer('all-MiniLM-L6-v2')
THRESHOLD = 0.4


def embed_text(text):

    # embedding the text and initialize the similarities matrix
    embeddings = model.encode(text)
    similarities_matrix = cosine_similarity(embeddings)
    collections = []

    for i in range(len(text)):
        for j in range(i + 1, len(text)):
            score = similarities_matrix[i][j]
            if score > THRESHOLD:
                collections.append((i, j, score))

    return list(collections)