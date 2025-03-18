from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

def vectorize_text(text):
    embeddings = OpenAIEmbeddings()
    vector = embeddings.embed(text)
    return vector

def save_to_chromadb(vector, metadata, db_path='chromadb'):
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    
    db = Chroma(persist_directory=db_path)
    db.add_texts(texts=[metadata['text']], embeddings=[vector], metadatas=[metadata])
    db.persist()