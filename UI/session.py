import streamlit as st


def initialize_session():
    """
    Initialize all session state variables.
    """

    defaults = {
        "user": None,
        "messages": [],
        "authenticated": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_chat():
    """
    Clears only the current conversation.
    """

    st.session_state.messages = []

    # Optional welcome message after clearing
    if st.session_state.user:

        user = st.session_state.user

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content":
                    f"Hello **{user['name']}** 👋\n\n"
                    f"You are logged in as **{user['department']}**.\n\n"
                    "How may I help you today?"
            }
        )


def logout():
    """
    Clears the entire session.
    """

    st.session_state.clear()