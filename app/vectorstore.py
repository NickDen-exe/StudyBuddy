import os
import chromadb
from app.embeddings import get_embeddings

os.environ["ANONYMIZED_TELEMETRY"] = "False"

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "study_materials"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def build_id(data):
    location = data.get("page", data.get("paragraph", 0))
    return f"{data['source']}_{location}_{data['chunk_index']}"


def build_metadata(data):
    return {
        "source": data["source"],
        "location": data.get("page", data.get("paragraph", 0)),
        "chunk_index": data["chunk_index"],
    }


def add_chunks(chunked_data):
    data_to_add = [data for data in chunked_data if not data["is_corrupted"]]

    ids = [build_id(data) for data in data_to_add]
    documents = [data["text"] for data in data_to_add]
    metadatas = [build_metadata(data) for data in data_to_add]
    embeddings = get_embeddings(documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(data_to_add)

def search(query, n_results=5):
    query_embedding = get_embeddings([query])
    results = collection.query(
        query_embeddings = query_embedding, 
        n_results=n_results,
    )
    return results