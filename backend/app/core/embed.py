from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# using the model 'all-MiniLM-L6-v2' for embedding
# having the threshold as 0.4
model = SentenceTransformer('all-MiniLM-L6-v2')
THRESHOLD = 0.4


def embed_text(text: list) -> list:

    # embedding the text and initialize the similarities matrix
    embeddings = model.encode(text)
    similarities_matrix = cosine_similarity(embeddings)
    collections = []

    for i in range(len(text)):
        for j in range(i + 1, len(text)):
            score = round(float(similarities_matrix[i][j]))
            if score > THRESHOLD:
                collections.append((i, j, score))

    return list(collections)

def clean_embed(coll):
    evecol = []

    for i in range(len(coll)):
        alr = set()

        if coll[i][1] not in alr or coll[i][2] not in alr:
            if coll[i][1] not in alr:
                alr.add(coll[i][1])
            if coll[i][2] not in alr:
                alr.add(coll[i][2])

        if list(alr) not in evecol:
            evecol.append(list(alr))

    return evecol