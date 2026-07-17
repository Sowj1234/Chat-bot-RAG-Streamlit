import streamlit as st

from UI.sidebar import render_sidebar
from UI.session import (
    initialize_session,
    clear_chat,
    logout
)
from UI.login import render_login
from UI.chat import render_chat

from rag.retrieval import RAGRetriever
from rag.embedding_manager import EmbeddingManager
from rag.vector_store import VectorStore


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Role Based Chatbot",
    layout="wide"
)


# --------------------------------------------------
# Initialize Session
# --------------------------------------------------

initialize_session()


# --------------------------------------------------
# Load RAG Components (only once)
# --------------------------------------------------

@st.cache_resource
def load_rag():

    embedding_manager = EmbeddingManager()
    print("EmbeddingManager created")

    vector_store = VectorStore()
    print("VectorStore created")

    retriever = RAGRetriever(
        vector_store,
        embedding_manager
    )

    print("RAGRetriever created")

    return retriever


rag_retriever = load_rag()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

action = render_sidebar()

if action == "clear_chat":

    clear_chat()
    st.rerun()

elif action == "logout":

    logout()
    st.rerun()


# --------------------------------------------------
# Main UI
# --------------------------------------------------

st.title("FinSolve Technologies AI Assistant")


# User not logged in
if not st.session_state.authenticated:

    render_login()

# Logged in
else:

    render_chat(rag_retriever)
