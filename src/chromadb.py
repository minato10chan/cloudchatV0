import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from datetime import datetime
from .types import DocumentMetadata
import uuid

class VectorStore:
    def __init__(self, collection_name: str = "chat_history"):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./data"
        ))
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        if not metadatas:
            metadatas = [{}] * len(texts)
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=[f"id_{i}" for i in range(len(texts))]
        )

    def add_document(self, text: str, metadata: DocumentMetadata):
        """Add a document with metadata to the collection"""
        doc_id = str(uuid.uuid4())
        
        self.collection.add(
            documents=[text],
            metadatas=[{
                "area": metadata.area,
                "major_category": metadata.major_category,
                "sub_category": metadata.sub_category,
                "source": metadata.source,
                "filename": metadata.filename,
                "upload_date": metadata.upload_date
            }],
            ids=[doc_id]
        )
        return doc_id

    def search(self, query: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def search_by_metadata(self, 
                          query: str, 
                          area: str = None, 
                          major_category: str = None,
                          sub_category: str = None,
                          n_results: int = 3):
        """Search documents with metadata filtering"""
        where = {}
        if area:
            where["area"] = area
        if major_category:
            where["major_category"] = major_category
        if sub_category:
            where["sub_category"] = sub_category

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where if where else None
        )
        return results
