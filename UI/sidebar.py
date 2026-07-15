import streamlit as st


def render_sidebar():
    """
    Render the left sidebar.
    Returns:
        action (str or None): "clear_chat", "logout", or None
    """

    action = None

    with st.sidebar:

        st.title("🤖 Company AI")

        st.divider()

        # --------------------------
        # User Information
        # --------------------------

        
        user = st.session_state.get("user")

        if user :
                st.markdown(f"### 👤 {user['name']}")
                st.write(f"**Employee ID:** {user['employee_id']}")
                st.write(f"**Role:** {user['role']}")
                st.write(f"**Department:** {user['department']}")

        else:

            st.info("Not logged in")

        st.divider()

        # --------------------------
        # Chat Actions
        # --------------------------

        if st.button("🗑 Clear Chat", use_container_width=True):
            action = "clear_chat"

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            action = "logout"

    return action