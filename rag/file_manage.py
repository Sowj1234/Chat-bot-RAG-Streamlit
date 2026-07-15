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

from typing import List, Dict, Any
from qdrant_client.models import Filter, FieldCondition, MatchValue

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def process_all_docs(directory, domain):
    all_docs = []
    doc_dir = Path(directory)

    # Process TXT files
    for file in doc_dir.glob("*.md"):
        try:
            loader = TextLoader(str(file), encoding="utf-8")
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file.name
                doc.metadata["file_type"] = "md"
                doc.metadata["domain"] = domain

            all_docs.extend(docs)

        except Exception as e:
            print(f"Error processing {file.name}: {e}")

    # Process CSV files
    for file in doc_dir.glob("*.csv"):
        try:
            loader = CSVLoader(str(file))
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file.name
                doc.metadata["file_type"] = "csv"
                doc.metadata["domain"] = domain

            all_docs.extend(docs)

        except Exception as e:
            print(f"Error processing {file.name}: {e}")

    # Process PDF files
    for file in doc_dir.glob("*.pdf"):
        try:
            loader = PyPDFLoader(str(file))
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file.name
                doc.metadata["file_type"] = "pdf"
                doc.metadata["domain"] = domain

            all_docs.extend(docs)
            

        except Exception as e:
            print(f"Error processing {file.name}: {e}")

    print(f"{domain}: Loaded {len(all_docs)} documents")
    return all_docs


##domain_docs={}
#for domain in {"marketing","HR","general","finance","engineering"}:
#    domain_docs[domain]=process_all_docs(f"../data/{domain}",domain)  

def load_all_domains():

    domain_docs = {}

    for domain in ["HR","general","finance","engineering","marketing"]:

        domain_docs[domain] = process_all_docs(
            DATA_DIR / domain,
            domain
        )

    return domain_docs  

def get_all_documents():
    domain_docs = load_all_domains()

    all_documents = []

    for domain, docs in domain_docs.items():
        if domain == "HR" or domain == "general" or domain == "finance" or domain == "marketing":
            continue
        all_documents.extend(docs)

    print(f"Total documents: {len(all_documents)}")

    return all_documents





#csv files are treated in row wise , there r 100 rows so 100 docs will be created for each csv file. Each doc will have metadata as source, file_type and domain.


def split_documents(docs, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    
    split_docs = text_splitter.split_documents(docs)
    for doc in split_docs:
        doc.metadata["chunk_id"] = str(uuid.uuid4())
    print(f"Document split into {len(split_docs)} chunks")
     # Show example of a chunk
    if split_docs:
        print(f"\nExample chunk:")
        print(f"Content: {split_docs[0].page_content[:200]}...")
        print(f"Metadata: {split_docs[0].metadata}")
    
    return split_docs

#document (str): The text document to process
#chunk_size (int): The target size of each chunk in characters
#chunk_overlap (int): The number of characters of overlap between chunks

#These separators are used by the RecursiveCharacterTextSplitter in LangChain to decide where to split a document into chunks.
#"\n\n" (Paragraph break)
#"\n" (Line break)
#" " (Space)
#"" (Empty string)

    
#all_chunks={} 
#{} is a dictionary that will store the split chunks of documents for each domain. The keys of the dictionary are the domain names (e.g., "HR", "general", "finance", "engineering"), and the values are lists of document chunks obtained by splitting the documents in that domain.

#for domain in {"HR","general","finance","engineering","marketing"}:
#    all_chunks[domain] = split_documents(domain_docs[domain], chunk_size=1000, chunk_overlap=200)

def chunk_all_domains(domain_docs):

    all_chunks = {}

    for domain in domain_docs:

        all_chunks[domain] = split_documents(
            domain_docs[domain],
            chunk_size=1000,
            chunk_overlap=200
        )

    return all_chunks


def get_all_chunks():
    """
    Loads every domain, splits them into chunks,
    and returns one combined list of LangChain Documents.
    """

    domain_docs = load_all_domains()

    all_chunks = chunk_all_domains(domain_docs)

    combined_chunks = []

    for domain in all_chunks:
        combined_chunks.extend(all_chunks[domain])

    print(f"\nTotal chunks: {len(combined_chunks)}")

    return combined_chunks