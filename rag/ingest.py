
from rag.embedding_manager import EmbeddingManager
from rag.file_manage import chunk_all_domains
from rag.file_manage import load_all_domains
from rag.vector_store import VectorStore

vector_store = VectorStore()

domain_docs = load_all_domains()
all_chunks = chunk_all_domains(domain_docs)



embedding_manager = EmbeddingManager()
print("EmbeddingManager created")

for domain, chunks in all_chunks.items():

    texts = [doc.page_content for doc in chunks]

    embeddings = embedding_manager.generate_embeddings(texts)

    vector_store.add_documents(chunks, embeddings)

    print(f"{domain} uploaded successfully")