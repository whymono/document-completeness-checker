from sentence_transformers import SentenceTransformer, util

# using the model 'all-MiniLM-L6-v2' for embedding
# having the threshold as 0.4
model = SentenceTransformer('all-MiniLM-L6-v2')
THRESHOLD = 0.7

# embedding the text and initialize the similarities matrix
def embed_text(text: list) -> list:

    embeddings = model.encode(text, convert_to_tensor=True)
    collections = []

    clusters = util.community_detection(embeddings, min_community_size=2, threshold=THRESHOLD)

    return clusters
