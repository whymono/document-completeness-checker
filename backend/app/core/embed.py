from sentence_transformers import SentenceTransformer, util

# using the model 'all-MiniLM-L6-v2' for embedding
# having the threshold as 0.4
model = SentenceTransformer('all-MiniLM-L6-v2')
THRESHOLD = 0.4

# embedding the text and initialize the similarities matrix
def embed_text(text: list) -> list:

    embeddings = model.encode(text, convert_to_tensor=True)
    collections = []

    clusters = util.community_detection(embeddings, min_community_size=2, threshold=THRESHOLD)

    return clusters

"""
# clean the embed_text output and return only necessary metrix
def clean_embed(coll: list) -> list:
    # evecol is the list of lists that contain 2 indexes of the similar sections
    evecol = []

    # this sorts the sections
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
"""

"""
    for i in range(len(text)):
        for j in range(i + 1, len(text)):
            score = round(float(similarities_matrix[i][j]))
            if score > THRESHOLD:
                collections.append((i, j, score))
"""
