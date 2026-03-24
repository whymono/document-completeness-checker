import math
from google import genai
from app.core.config import settings

THRESHOLD = 0.7

def _get_communities(embeddings: list, min_community_size: int = 2, threshold: float = 0.7) -> list:
    n = len(embeddings)
    if n == 0:
        return []
    
    # Compute similarity matrix
    dot_products = [[sum(a * b for a, b in zip(e1, e2)) for e2 in embeddings] for e1 in embeddings]
    norms = [math.sqrt(sum(a * a for a in e)) for e in embeddings]
    
    sim_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if norms[i] == 0 or norms[j] == 0:
                row.append(0.0)
            else:
                row.append(dot_products[i][j] / (norms[i] * norms[j]))
        sim_matrix.append(row)
        
    communities = []
    for i in range(n):
        members = [j for j in range(n) if sim_matrix[i][j] >= threshold]
        communities.append(members)
        
    # Sort nodes by community size in descending order
    sorted_nodes = sorted(range(n), key=lambda x: len(communities[x]), reverse=True)
    
    clusters = []
    assigned = [False] * n
    
    for node in sorted_nodes:
        if not assigned[node]:
            current_cluster = [m for m in communities[node] if not assigned[m]]
            if len(current_cluster) >= min_community_size:
                clusters.append(current_cluster)
                for m in current_cluster:
                    assigned[m] = True
                    
    return clusters

# embedding the text and initialize the similarities matrix
def embed_text(text: list) -> list:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    embeddings = [emb.values for emb in response.embeddings]

    clusters = _get_communities(embeddings, min_community_size=2, threshold=THRESHOLD)

    return clusters
