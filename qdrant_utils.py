import qdrant_client
from qdrant_client.http import models
from llama_cpp import Llama

# Set up the Qdrant client and collection configuration
client = qdrant_client.QdrantClient(url="localhost:6333")
collection_config = models.VectorParams(size=384, distance=models.Distance.DOT)

# Qdrant collection name
QdrantCollName = "testcollections"

def vectorize_content(id, content):
    """
    Vectorizes the provided content using the Llama model and returns the vector and ID.
    """
    model_path = "bge-small-en-v1.5-q4_k_m.gguf"
    model = Llama(model_path, embedding=True)
    embedding = model.embed(content)
    return id, embedding

def send_db(payload):
    """
    Vectorizes the content and sends it to the Qdrant database with the provided ID.
    """
    id, vector = vectorize_content(payload["id"], payload["content"])
    if not client.collection_exists(collection_name=QdrantCollName):
        client.create_collection(collection_name=QdrantCollName, vectors_config=collection_config)
    client.upsert(
        collection_name=QdrantCollName, 
        points=[models.PointStruct(id=id, vector=vector, payload=payload)]
    )

def delete_vector(vector_id):
    """
    Deletes a vector from the Qdrant database based on the provided vector ID.
    """
    try:
        client.delete(
            collection_name=QdrantCollName,
            points_selector=models.PointIdsList(
        points=[vector_id])
        )
        return {"status": "Vector deleted successfully", "vector_id": vector_id}
    except Exception as e:
        return {"error": str(e)}

def similarity(data):
    """
    Searches the Qdrant database for similar content based on the vectorized input and returns the top results.
    """
    try:
        id, embedding = vectorize_content(data["user_id"], data["content"])
        search = client.search(
            collection_name=QdrantCollName,
            search_params=models.SearchParams(hnsw_ef=128, exact=False),
            query_vector=embedding,
            limit=3
        )

        if not search:
            return {"message": "No similar content found."}
        
        data = {point.id: point.score for point in search}
        return data
    except Exception as e:
        return {"error": str(e)}
