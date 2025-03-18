from chromadb import Client
from chromadb.config import Settings

class ChromaDBManager:
    def __init__(self, db_url: str):
        self.client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=db_url))

    def save_vector(self, collection_name: str, vector: list, metadata: dict):
        collection = self.client.get_or_create_collection(collection_name)
        collection.add(
            documents=[metadata['document']],
            embeddings=[vector],
            metadatas=[metadata]
        )

    def get_vector(self, collection_name: str, document: str):
        collection = self.client.get_collection(collection_name)
        results = collection.query(
            query_embeddings=[document],
            n_results=1
        )
        return results

    def list_collections(self):
        return self.client.list_collections()