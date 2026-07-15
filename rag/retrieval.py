import os
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader, TextLoader,CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
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
from typing import List, Dict, Any
from qdrant_client.models import Filter, FieldCondition, MatchValue

from rag.embedding_manager import EmbeddingManager
from rag.vector_store import VectorStore

class RAGRetriever:
    """Handles query-based retrieval from the vector store"""

    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        """
        Initialize the retriever

        Args:
            vector_store: Vector store containing document embeddings
            embedding_manager: Manager for generating query embeddings
        """
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(
        self,
        query,
        top_k=5,
        score_threshold=0.1,
        domain=None
    ):
        """
        Retrieve documents based on a query

        Args:
            query: The search query string
            top_k: Number of top results to return
            score_threshold: Minimum similarity score for results
            domain: Optional domain filter for retrieval
        """

        # Generate query embedding
        query_embedding = self.embedding_manager.generate_embeddings([query])[0]
        print(f"Query embedding generated for query: '{query_embedding}'")
        # Apply domain filter if provided
        search_filter = None
        domain = domain.lower()
        if domain:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="domain",
                        match=MatchValue(value=domain)
                    )
                ]
            )

        # Search Qdrant
        results = self.vector_store.client.query_points(
            collection_name=self.vector_store.collection_name,
            query=query_embedding.tolist(),
            limit=top_k
        )
        print(f"Retrieved {len(results.points)} results for query: '{query}' with domain filter: '{domain}'")

        for result in results.points:
           print("Score:", result.score)

        # Process results
        retrieved_docs = []

        for rank, result in enumerate(results.points, start=1):

            if result.score >= score_threshold:

                payload = result.payload

                retrieved_docs.append({
                    "id": result.id,
                    "content": payload["text"],
                    "metadata": payload,
                    "similarity_score": result.score,
                    "rank": rank
                })

        return retrieved_docs
    
"""vector_store=VectorStore()
embedding_manager=EmbeddingManager()


rag_retriever = RAGRetriever(vector_store=vector_store, embedding_manager=embedding_manager)
rag_retriever


rag_retriever.retrieve(
    "What was the marketing spend in Q4 2024?",
    domain="marketing"
)"""