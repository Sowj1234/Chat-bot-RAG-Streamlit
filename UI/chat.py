import streamlit as st

from access_control import validate_query
from rag.rag_pipeline import rag_simple


def render_chat(rag_retriever):

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask something...")

    if not user_query:
        return

    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_query
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    department = st.session_state.user["department"]

    validation = validate_query(
        department,
        user_query
    )

    if validation["allowed"]:

        response = rag_simple(

            query=user_query,

            retriever=rag_retriever,

            domain=department,

            top_k=3
        )

    else:

        reason = validation["reason"]

        if reason == "ACCESS_DENIED":

            response = (
                "You do not have permission "
                "to access another department."
            )

        elif reason == "OUT_OF_SCOPE":

            response = (
                "I can only answer company-related questions."
            )

        else:

            response = (
                "Your request violates "
                "the chatbot security policy."
            )

    st.session_state.messages.append(

        {
            "role":"assistant",
            "content":response
        }

    )

    with st.chat_message("assistant"):
        st.markdown(response)