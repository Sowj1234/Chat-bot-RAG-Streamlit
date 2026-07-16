import os
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader, TextLoader,CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pathlib import Path

from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader,
    CSVLoader,
    PyPDFLoader
)

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import uuid
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict ,Any, Tuple
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from rag.file_manage import load_all_domains,chunk_all_domains 
from rag.embedding_manager import EmbeddingManager

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class VectorStore:
    """Manages document embeddings in Qdrant"""

    def __init__(
        self,
        collection_name="company_docs",
        persist_directory= BASE_DIR / "data" / "qdrant_db2",
        embedding_dim=384
    ):

        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_dim = embedding_dim

        self.client = None

        self._initialize_store()
    
    def _initialize_store(self):

        print("cwd:", os.getcwd())
        print("persist:", os.path.abspath(self.persist_directory))
        
        os.makedirs(self.persist_directory, exist_ok=True)
        self.client = QdrantClient(path=self.persist_directory)
        collections = self.client.get_collections().collections

        names = [c.name for c in collections]
        
        if self.collection_name not in names:

            self.client.create_collection(
                collection_name=self.collection_name,

                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=Distance.COSINE
                )
            )

            print("Collection created.")

        else:
            print("Collection already exists.")
    

    def add_documents(self,documents: List[Any],embeddings: np.ndarray):
        """
        Add documents and their embeddings to the vector store
        
        Args:
            documents: List of LangChain documents
            embeddings: Corresponding embeddings for the documents
        """
        
        if len(documents) != len(embeddings):
            raise ValueError(
                "Documents and embeddings count mismatch."
            )

        points = []

        for doc, embedding in zip(documents, embeddings):
            payload = {
                "text": doc.page_content,
                **doc.metadata
            }
            point = PointStruct(

                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload=payload
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(f"Inserted {len(points)} documents.")

#initialising vector store
"""vector_store = VectorStore()
vector_store

domain_docs=load_all_domains("../data/docs")
all_chunks=chunk_all_domains(domain_docs)

embedding_manager=EmbeddingManager()
for domain, chunks in all_chunks.items():

    texts = [doc.page_content for doc in chunks]

    embeddings = embedding_manager.generate_embeddings(texts)

    vector_store.add_documents(chunks, embeddings)

    print(f"{domain} uploaded successfully")"""