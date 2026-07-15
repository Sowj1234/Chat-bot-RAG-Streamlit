import json
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
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


load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")
llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant", temperature=0.1)

def rag_simple(query,retriever,domain,top_k=3):
    results=retriever.retrieve(query,top_k=top_k,domain=domain)
    #combining all the top k results into a single context string, separated by two newlines. This context will be used to answer the query.
    context="\n\n".join([doc['content'] for doc in results]) if results else ""
    if not context:
        return "No relevant context found to answer the question."
    
    prompt=f"""Use the following context to answer the question concisely.
        Context:
        {context}

        Question: {query}

        Answer:"""
    
    response=llm.invoke(prompt)
    return response.content
