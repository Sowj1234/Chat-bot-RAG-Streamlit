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


class EmbeddingManager:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize the embedding manager
        Args:
            model_name: HuggingFace model name for sentence embeddings
        """
        self.model_name = model_name
        self.model =None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try: 
            self.model = SentenceTransformer(self.model_name)
            print(f"Loaded model: {self.model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts
        Args:
            texts: List of text strings
            Returns:
            numpy array of embeddings with shape (len(texts), embedding_dim)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call _load_model() first.")
        
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Generated embeddings with shape: {embeddings.shape}")
        return embeddings
    

    #initialise the embeedding manager
#embedding_manager = EmbeddingManager(model_name="all-MiniLM-L6-v2")
#embedding_manager