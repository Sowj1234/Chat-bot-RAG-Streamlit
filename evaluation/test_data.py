import os
import sys
sys.path.append("..")
from rag.file_manage import  get_all_documents
import langchain_google_vertexai
# Fake the old module location for legacy libraries
sys.modules['langchain_community.chat_models.vertexai'] = langchain_google_vertexai

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.testset import TestsetGenerator

from dotenv import load_dotenv
import os

load_dotenv()


#better reasoning , better question generation , fewer hallucinations ,deterministic at temperature=0
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)
#embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


generator_llm = LangchainLLMWrapper(llm)
generator_embeddings = LangchainEmbeddingsWrapper(
    embedding_model
)



documents =  get_all_documents()

print(len(documents))

generator = TestsetGenerator(
    llm=generator_llm,
    embedding_model=generator_embeddings
)

testset = generator.generate_with_langchain_docs(
    documents=documents,
    testset_size=2,
)

df = testset.to_pandas()

print(df.head())
print(df.iloc[0])

df.to_csv("synthetic_testset.csv", index=False)